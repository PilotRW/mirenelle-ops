from collections import defaultdict
from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.models.amazon_payment_transaction import AmazonPaymentTransaction
from app.models.inventory_item import InventoryItem
from app.models.product_mapping import ProductMapping
from app.models.purchase_invoice_line import PurchaseInvoiceLine
from app.services.product_mapping_service import product_similarity
from app.services.transaction_classifier import is_order_payment


router = APIRouter(prefix="/inventory", tags=["inventory"])


class InventoryItemRequest(BaseModel):
    sku: str = Field(min_length=1, max_length=160)
    ean: str | None = Field(default=None, max_length=64)
    asin: str | None = Field(default=None, max_length=32)
    product_name: str | None = None
    marketplace: str = Field(default="EU", min_length=2, max_length=16)
    fulfillment_channel: str = Field(default="FBA", min_length=2, max_length=40)
    quantity_on_hand: float = Field(ge=0)
    quantity_reserved: float = Field(default=0, ge=0)
    quantity_inbound: float = Field(default=0, ge=0)
    reorder_point: float = Field(default=0, ge=0)
    notes: str | None = None


class InventoryItemRow(BaseModel):
    id: int
    sku: str
    ean: str | None
    asin: str | None
    product_name: str | None
    marketplace: str
    fulfillment_channel: str
    purchased_quantity: float
    sold_quantity: float
    quantity_on_hand: float
    quantity_reserved: float
    quantity_available: float
    quantity_inbound: float
    reorder_point: float
    status: str
    notes: str | None
    updated_at: str


class InventoryListResponse(BaseModel):
    rows: list[InventoryItemRow]


class InventorySummaryResponse(BaseModel):
    products: int
    total_on_hand: float
    total_available: float
    total_inbound: float
    low_stock: int
    out_of_stock: int


class DeleteInventoryItemResponse(BaseModel):
    item_id: int
    deleted: bool


class SyncInventoryResponse(BaseModel):
    products: int
    created: int
    updated: int
    sales_matched: float
    sales_unmatched: float


def clean_text(value: str | None) -> str | None:
    return (value or "").strip() or None


def inventory_status(item: InventoryItem) -> str:
    available = (item.quantity_on_hand or Decimal("0")) - (item.quantity_reserved or Decimal("0"))
    if available <= 0:
        return "out_of_stock"
    if item.reorder_point and available <= item.reorder_point:
        return "low_stock"
    return "healthy"


def inventory_row(
    item: InventoryItem,
    purchased_quantity: Decimal | None = None,
    sold_quantity: Decimal | None = None,
) -> InventoryItemRow:
    available = (item.quantity_on_hand or Decimal("0")) - (item.quantity_reserved or Decimal("0"))
    return InventoryItemRow(
        id=item.id,
        sku=item.sku,
        ean=item.ean,
        asin=item.asin,
        product_name=item.product_name,
        marketplace=item.marketplace,
        fulfillment_channel=item.fulfillment_channel,
        purchased_quantity=float(purchased_quantity or 0),
        sold_quantity=float(sold_quantity or 0),
        quantity_on_hand=float(item.quantity_on_hand or 0),
        quantity_reserved=float(item.quantity_reserved or 0),
        quantity_available=float(available),
        quantity_inbound=float(item.quantity_inbound or 0),
        reorder_point=float(item.reorder_point or 0),
        status=inventory_status(item),
        notes=item.notes,
        updated_at=item.updated_at.isoformat(),
    )


def apply_inventory_payload(item: InventoryItem, payload: InventoryItemRequest) -> None:
    item.sku = payload.sku.strip()
    item.ean = clean_text(payload.ean)
    item.asin = clean_text(payload.asin)
    item.product_name = clean_text(payload.product_name)
    item.marketplace = payload.marketplace.strip().upper()
    item.fulfillment_channel = payload.fulfillment_channel.strip().upper()
    item.quantity_on_hand = Decimal(str(payload.quantity_on_hand))
    item.quantity_reserved = Decimal(str(payload.quantity_reserved))
    item.quantity_inbound = Decimal(str(payload.quantity_inbound))
    item.reorder_point = Decimal(str(payload.reorder_point))
    item.notes = clean_text(payload.notes)


def best_purchased_match(product_details_aliases: set[str], candidates: list[tuple[str, str]]) -> str | None:
    if not product_details_aliases:
        return None
    best_sku = None
    best_score = Decimal("0")
    for product_details in product_details_aliases:
        for product_name, sku in candidates:
            score = product_similarity(product_details, product_name)
            if score > best_score:
                best_score = score
                best_sku = sku
    return best_sku if best_score >= Decimal("55") else None


async def calculate_inventory_quantities(
    db: AsyncSession,
) -> tuple[dict[str, dict], defaultdict[str, Decimal], Decimal, Decimal]:
    purchased: dict[str, dict] = {}
    purchased_candidates: list[tuple[str, str]] = []
    invoice_lines = await db.scalars(
        select(PurchaseInvoiceLine)
        .where(PurchaseInvoiceLine.line_type == "product")
        .where(
            PurchaseInvoiceLine.sku.is_not(None)
            | PurchaseInvoiceLine.supplier_sku.is_not(None)
            | PurchaseInvoiceLine.ean.is_not(None)
        )
    )
    for line in invoice_lines:
        sku = (line.sku or line.supplier_sku or line.ean or "").strip()
        if not sku:
            continue
        if sku not in purchased:
            purchased[sku] = {
                "sku": sku,
                "ean": line.ean,
                "product_name": line.product_name,
                "quantity": Decimal("0"),
            }
        purchased[sku]["quantity"] += line.quantity or Decimal("0")
        if line.ean:
            purchased[sku]["ean"] = line.ean
        if line.product_name:
            purchased[sku]["product_name"] = line.product_name

    for sku, values in purchased.items():
        product_name = values.get("product_name")
        if product_name:
            purchased_candidates.append((product_name, sku))

    mapped_product_skus: dict[str, str] = {}
    mapping_rows = await db.scalars(select(ProductMapping).order_by(ProductMapping.id.desc()))
    for mapping in mapping_rows:
        mapped_sku = (mapping.sku or mapping.supplier_sku or mapping.ean or "").strip()
        if mapped_sku and mapped_sku in purchased:
            mapped_product_skus.setdefault(mapping.amazon_product_details, mapped_sku)

    sold_by_sku: defaultdict[str, Decimal] = defaultdict(lambda: Decimal("0"))
    sales_matched = Decimal("0")
    sales_unmatched = Decimal("0")
    sales_buckets: dict[str, dict] = {}
    payment_rows = await db.scalars(
        select(AmazonPaymentTransaction)
        .where(AmazonPaymentTransaction.sku.is_not(None))
        .where(AmazonPaymentTransaction.quantity.is_not(None))
    )
    for payment in payment_rows:
        if not is_order_payment(payment.transaction_type):
            continue
        sku = (payment.sku or "").strip()
        if not sku:
            continue
        bucket = sales_buckets.setdefault(
            sku,
            {
                "quantity": Decimal("0"),
                "product_details_aliases": set(),
            },
        )
        bucket["quantity"] += abs(payment.quantity or Decimal("0"))
        if payment.product_details:
            bucket["product_details_aliases"].add(str(payment.product_details))

    for sku, bucket in sales_buckets.items():
        quantity = bucket["quantity"]
        product_details_aliases = set(bucket["product_details_aliases"])
        product_details_aliases.add(sku)
        matched_sku = (
            sku
            if sku in purchased
            else next(
                (
                    mapped_product_skus[alias]
                    for alias in product_details_aliases
                    if alias in mapped_product_skus
                ),
                None,
            )
            or best_purchased_match(product_details_aliases, purchased_candidates)
        )
        if matched_sku:
            sold_by_sku[matched_sku] += quantity
            sales_matched += quantity
        else:
            sales_unmatched += quantity

    return purchased, sold_by_sku, sales_matched, sales_unmatched


@router.get("/items", response_model=InventoryListResponse)
async def list_inventory_items(
    db: Annotated[AsyncSession, Depends(get_db)],
    query: Annotated[str | None, Query()] = None,
    marketplace: Annotated[str | None, Query()] = None,
) -> InventoryListResponse:
    statement = select(InventoryItem).order_by(InventoryItem.marketplace, InventoryItem.sku)
    if query:
        pattern = f"%{query}%"
        statement = statement.where(
            InventoryItem.sku.ilike(pattern)
            | InventoryItem.ean.ilike(pattern)
            | InventoryItem.asin.ilike(pattern)
            | InventoryItem.product_name.ilike(pattern)
        )
    if marketplace and marketplace.upper() != "ALL":
        statement = statement.where(InventoryItem.marketplace == marketplace.upper())
    result = await db.scalars(statement)
    purchased, sold_by_sku, _, _ = await calculate_inventory_quantities(db)
    return InventoryListResponse(
        rows=[
            inventory_row(
                item,
                purchased_quantity=purchased.get(item.sku, {}).get("quantity", Decimal("0")),
                sold_quantity=sold_by_sku[item.sku],
            )
            for item in result
        ]
    )


@router.get("/summary", response_model=InventorySummaryResponse)
async def inventory_summary(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> InventorySummaryResponse:
    items = list(await db.scalars(select(InventoryItem)))
    total_on_hand = Decimal("0")
    total_available = Decimal("0")
    total_inbound = Decimal("0")
    low_stock = 0
    out_of_stock = 0
    for item in items:
        available = (item.quantity_on_hand or Decimal("0")) - (item.quantity_reserved or Decimal("0"))
        total_on_hand += item.quantity_on_hand or Decimal("0")
        total_available += available
        total_inbound += item.quantity_inbound or Decimal("0")
        status = inventory_status(item)
        low_stock += 1 if status == "low_stock" else 0
        out_of_stock += 1 if status == "out_of_stock" else 0
    return InventorySummaryResponse(
        products=len(items),
        total_on_hand=float(total_on_hand),
        total_available=float(total_available),
        total_inbound=float(total_inbound),
        low_stock=low_stock,
        out_of_stock=out_of_stock,
    )


@router.post("/items", response_model=InventoryItemRow)
async def upsert_inventory_item(
    payload: InventoryItemRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> InventoryItemRow:
    sku = payload.sku.strip()
    marketplace = payload.marketplace.strip().upper()
    fulfillment_channel = payload.fulfillment_channel.strip().upper()
    item = await db.scalar(
        select(InventoryItem)
        .where(InventoryItem.sku == sku)
        .where(InventoryItem.marketplace == marketplace)
        .where(InventoryItem.fulfillment_channel == fulfillment_channel)
    )
    if item is None:
        item = InventoryItem(sku=sku, marketplace=marketplace, fulfillment_channel=fulfillment_channel)
        db.add(item)
    apply_inventory_payload(item, payload)
    await db.commit()
    await db.refresh(item)
    purchased, sold_by_sku, _, _ = await calculate_inventory_quantities(db)
    return inventory_row(
        item,
        purchased_quantity=purchased.get(item.sku, {}).get("quantity", Decimal("0")),
        sold_quantity=sold_by_sku[item.sku],
    )


@router.post("/sync-from-invoices", response_model=SyncInventoryResponse)
async def sync_inventory_from_invoices(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> SyncInventoryResponse:
    purchased, sold_by_sku, sales_matched, sales_unmatched = await calculate_inventory_quantities(db)

    created = 0
    updated = 0
    for sku, values in purchased.items():
        item = await db.scalar(
            select(InventoryItem)
            .where(InventoryItem.sku == sku)
            .where(InventoryItem.marketplace == "EU")
            .where(InventoryItem.fulfillment_channel == "FBA")
        )
        if item is None:
            item = InventoryItem(sku=sku, marketplace="EU", fulfillment_channel="FBA")
            db.add(item)
            created += 1
        else:
            updated += 1
        item.ean = values["ean"]
        item.product_name = values["product_name"]
        item.quantity_on_hand = max(Decimal("0"), values["quantity"] - sold_by_sku[sku])
        item.quantity_reserved = Decimal("0")
        item.quantity_inbound = Decimal("0")
        sold_quantity = sold_by_sku[sku]
        item.notes = (
            "Estimated from purchase invoices minus matched Amazon order quantities. "
            f"Purchased: {values['quantity']}; matched sold: {sold_quantity}."
        )

    await db.commit()
    return SyncInventoryResponse(
        products=len(purchased),
        created=created,
        updated=updated,
        sales_matched=float(sales_matched),
        sales_unmatched=float(sales_unmatched),
    )


@router.put("/items/{item_id}", response_model=InventoryItemRow)
async def update_inventory_item(
    item_id: int,
    payload: InventoryItemRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> InventoryItemRow:
    item = await db.get(InventoryItem, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Inventory item was not found.")
    apply_inventory_payload(item, payload)
    await db.commit()
    await db.refresh(item)
    purchased, sold_by_sku, _, _ = await calculate_inventory_quantities(db)
    return inventory_row(
        item,
        purchased_quantity=purchased.get(item.sku, {}).get("quantity", Decimal("0")),
        sold_quantity=sold_by_sku[item.sku],
    )


@router.delete("/items/{item_id}", response_model=DeleteInventoryItemResponse)
async def delete_inventory_item(
    item_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> DeleteInventoryItemResponse:
    item = await db.get(InventoryItem, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Inventory item was not found.")
    await db.delete(item)
    await db.commit()
    return DeleteInventoryItemResponse(item_id=item_id, deleted=True)
