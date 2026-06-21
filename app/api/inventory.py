from collections import defaultdict
from datetime import date
from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.models.amazon_order_item import AmazonOrderItem
from app.models.amazon_payment_transaction import AmazonPaymentTransaction
from app.models.bundle_component import BundleComponent
from app.models.bundle_assembly import BundleAssembly
from app.models.inventory_item import InventoryItem
from app.models.inventory_lot import InventoryLot
from app.models.product_mapping import ProductMapping
from app.models.purchase_invoice_line import PurchaseInvoiceLine
from app.services.product_mapping_service import product_similarity
from app.services.order_item_policy import partition_order_item_keys
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
    bundle_consumed_quantity: float
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


class OpeningLotRequest(BaseModel):
    sku: str = Field(min_length=1, max_length=160)
    ean: str | None = Field(default=None, max_length=64)
    product_name: str = Field(min_length=1)
    purchase_date: date
    quantity_received: float = Field(gt=0)
    unit_cost: float = Field(gt=0)
    currency: str = Field(default="EUR", min_length=3, max_length=8)
    notes: str | None = None


class OpeningLotRow(BaseModel):
    id: int
    sku: str | None
    ean: str | None
    product_name: str
    purchase_date: str
    quantity_received: float
    unit_cost: float
    currency: str
    notes: str | None


class OpeningLotListResponse(BaseModel):
    rows: list[OpeningLotRow]


class BundleComponentRequest(BaseModel):
    bundle_sku: str = Field(min_length=1, max_length=160)
    bundle_name: str | None = Field(default=None, max_length=500)
    component_sku: str = Field(min_length=1, max_length=160)
    component_quantity: float = Field(gt=0)


class BundleComponentRow(BaseModel):
    id: int
    bundle_sku: str
    bundle_name: str | None
    component_sku: str
    component_quantity: float


class BundleComponentListResponse(BaseModel):
    rows: list[BundleComponentRow]


class BundleRecipeComponentRequest(BaseModel):
    component_sku: str = Field(min_length=1, max_length=160)
    component_quantity: float = Field(gt=0)


class BundleRecipeRequest(BaseModel):
    bundle_sku: str = Field(min_length=1, max_length=160)
    bundle_name: str | None = Field(default=None, max_length=500)
    original_bundle_sku: str | None = Field(default=None, max_length=160)
    components: list[BundleRecipeComponentRequest] = Field(min_length=1)


class BundleCandidateRow(BaseModel):
    sku: str
    product_name: str | None


class ComponentCandidateRow(BaseModel):
    sku: str
    product_name: str
    available_quantity: float
    latest_unit_cost: float
    currency: str


class BundleCandidateResponse(BaseModel):
    bundles: list[BundleCandidateRow]
    components: list[ComponentCandidateRow]


class BundleAssemblyRequest(BaseModel):
    bundle_sku: str = Field(min_length=1, max_length=160)
    assembly_date: date
    quantity: float = Field(gt=0)
    assembly_provider: str = Field(default="prep_center", max_length=32)
    unit_assembly_cost: float = Field(default=0, ge=0)
    currency: str = Field(default="EUR", min_length=3, max_length=8)
    notes: str | None = None


class BundleAssemblyUpdateRequest(BaseModel):
    assembly_date: date
    assembly_provider: str = Field(default="prep_center", max_length=32)
    unit_assembly_cost: float = Field(default=0, ge=0)
    currency: str = Field(default="EUR", min_length=3, max_length=8)
    notes: str | None = None


class BundleAssemblyRow(BaseModel):
    id: int
    bundle_sku: str
    assembly_date: str
    quantity: float
    assembly_provider: str
    unit_assembly_cost: float
    currency: str
    notes: str | None


class BundleAssemblyListResponse(BaseModel):
    rows: list[BundleAssemblyRow]


def clean_text(value: str | None) -> str | None:
    return (value or "").strip() or None


def normalize_assembly_provider(value: str) -> str:
    provider = value.strip().lower()
    allowed_providers = {"unknown", "prep_center", "amazon", "in_house", "other"}
    if provider not in allowed_providers:
        raise HTTPException(
            status_code=422,
            detail="Assembly provider must be unknown, prep_center, amazon, in_house, or other.",
        )
    return provider


def opening_lot_row(lot: InventoryLot) -> OpeningLotRow:
    return OpeningLotRow(
        id=lot.id,
        sku=lot.sku,
        ean=lot.ean,
        product_name=lot.product_name,
        purchase_date=lot.purchase_date.isoformat(),
        quantity_received=float(lot.quantity_received),
        unit_cost=float(lot.unit_cost),
        currency=lot.currency,
        notes=lot.notes,
    )


def bundle_component_row(component: BundleComponent) -> BundleComponentRow:
    return BundleComponentRow(
        id=component.id,
        bundle_sku=component.bundle_sku,
        bundle_name=component.bundle_name,
        component_sku=component.component_sku,
        component_quantity=float(component.component_quantity),
    )


def bundle_assembly_row(assembly: BundleAssembly) -> BundleAssemblyRow:
    return BundleAssemblyRow(
        id=assembly.id,
        bundle_sku=assembly.bundle_sku,
        assembly_date=assembly.assembly_date.isoformat(),
        quantity=float(assembly.quantity),
        assembly_provider=assembly.assembly_provider,
        unit_assembly_cost=float(assembly.unit_assembly_cost),
        currency=assembly.currency,
        notes=assembly.notes,
    )


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
    bundle_consumed_quantity: Decimal | None = None,
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
        bundle_consumed_quantity=float(bundle_consumed_quantity or 0),
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


def bundle_component_sales(
    recipe: list[BundleComponent] | list[dict],
    bundle_quantity: Decimal,
    purchased: dict[str, dict],
) -> dict[str, Decimal] | None:
    component_sales: defaultdict[str, Decimal] = defaultdict(lambda: Decimal("0"))
    purchased_key_by_identifier: dict[str, str] = {}
    for purchased_sku, values in purchased.items():
        for identifier in (purchased_sku, values.get("ean")):
            clean_identifier = (identifier or "").strip()
            if clean_identifier:
                purchased_key_by_identifier.setdefault(clean_identifier, purchased_sku)

    for component in recipe:
        component_identifier = (
            component.get("component_sku")
            if isinstance(component, dict)
            else component.component_sku
        )
        component_identifier = (component_identifier or "").strip()
        purchased_sku = purchased_key_by_identifier.get(component_identifier)
        if not purchased_sku:
            return None
        component_quantity = (
            component.get("component_quantity")
            if isinstance(component, dict)
            else component.component_quantity
        )
        component_sales[purchased_sku] += (
            abs(bundle_quantity) * Decimal(str(component_quantity))
        )
    return dict(component_sales)


def split_bundle_component_consumption(
    sold_quantity: Decimal,
    assembly_quantity: Decimal,
) -> tuple[Decimal, Decimal]:
    return (
        max(Decimal("0"), sold_quantity - assembly_quantity),
        assembly_quantity,
    )


async def calculate_inventory_quantities(
    db: AsyncSession,
) -> tuple[
    dict[str, dict],
    defaultdict[str, Decimal],
    defaultdict[str, Decimal],
    Decimal,
    Decimal,
]:
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

    opening_lots = await db.scalars(
        select(InventoryLot).where(InventoryLot.source == "manual_opening")
    )
    for lot in opening_lots:
        sku = (lot.sku or lot.ean or "").strip()
        if not sku:
            continue
        if sku not in purchased:
            purchased[sku] = {
                "sku": sku,
                "ean": lot.ean,
                "product_name": lot.product_name,
                "quantity": Decimal("0"),
            }
        purchased[sku]["quantity"] += lot.quantity_received or Decimal("0")
        if lot.ean:
            purchased[sku]["ean"] = lot.ean
        purchased[sku]["product_name"] = lot.product_name

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
    assembled_by_sku: defaultdict[str, Decimal] = defaultdict(lambda: Decimal("0"))
    bundle_sales_by_sku: defaultdict[str, Decimal] = defaultdict(lambda: Decimal("0"))
    recipes_by_bundle: defaultdict[str, list[BundleComponent]] = defaultdict(list)
    for component in await db.scalars(
        select(BundleComponent).order_by(
            BundleComponent.bundle_sku,
            BundleComponent.component_sku,
        )
    ):
        recipes_by_bundle[(component.bundle_sku or "").strip()].append(component)
    sales_matched = Decimal("0")
    sales_unmatched = Decimal("0")
    sales_buckets: dict[str, dict] = {}
    order_items = list(await db.scalars(select(AmazonOrderItem)))
    known_order_keys, eligible_order_keys = partition_order_item_keys(order_items)
    payment_rows = await db.scalars(
        select(AmazonPaymentTransaction)
        .where(AmazonPaymentTransaction.sku.is_not(None))
        .where(AmazonPaymentTransaction.quantity.is_not(None))
    )
    for payment in payment_rows:
        if not is_order_payment(payment.transaction_type):
            continue
        order_key = (
            (payment.external_transaction_id or "").strip(),
            (payment.sku or "").strip(),
        )
        if order_key in known_order_keys and order_key not in eligible_order_keys:
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
        recipe = recipes_by_bundle.get(sku, [])
        if recipe:
            bundle_sales_by_sku[sku] += quantity
            sales_matched += quantity
            continue
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

    assembly_quantity_by_bundle: defaultdict[str, Decimal] = defaultdict(lambda: Decimal("0"))
    assemblies = await db.scalars(
        select(BundleAssembly).order_by(
            BundleAssembly.assembly_date,
            BundleAssembly.id,
        )
    )
    for assembly in assemblies:
        bundle_sku = (assembly.bundle_sku or "").strip()
        assembly_quantity_by_bundle[bundle_sku] += Decimal(str(assembly.quantity))
        assembly_components = bundle_component_sales(
            list(assembly.component_snapshot or []),
            Decimal(str(assembly.quantity)),
            purchased,
        )
        if assembly_components is None:
            continue
        for component_sku, component_quantity in assembly_components.items():
            assembled_by_sku[component_sku] += component_quantity

    for bundle_sku in set(bundle_sales_by_sku) | set(assembly_quantity_by_bundle):
        recipe = recipes_by_bundle.get(bundle_sku, [])
        assembly_quantity = assembly_quantity_by_bundle[bundle_sku]
        sold_quantity = bundle_sales_by_sku[bundle_sku]
        uncovered_sale_quantity, _ = (
            split_bundle_component_consumption(sold_quantity, assembly_quantity)
        )
        uncovered_sale_components = bundle_component_sales(
            recipe,
            uncovered_sale_quantity,
            purchased,
        )
        if uncovered_sale_components is None:
            if sold_quantity:
                sales_unmatched += sold_quantity
                sales_matched -= sold_quantity
            continue
        for component_sku, component_quantity in uncovered_sale_components.items():
            sold_by_sku[component_sku] += component_quantity

    return purchased, sold_by_sku, assembled_by_sku, sales_matched, sales_unmatched


async def update_estimated_inventory_items(
    db: AsyncSession,
    purchased: dict[str, dict],
    sold_by_sku: defaultdict[str, Decimal],
    assembled_by_sku: defaultdict[str, Decimal],
) -> tuple[int, int]:
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
        item.quantity_on_hand = max(
            Decimal("0"),
            values["quantity"] - sold_by_sku[sku] - assembled_by_sku[sku],
        )
        item.quantity_reserved = Decimal("0")
        item.quantity_inbound = Decimal("0")
        item.notes = (
            "Estimated from purchase invoices minus matched Amazon order quantities "
            "and recorded bundle assemblies. "
            f"Purchased: {values['quantity']}; matched sold: {sold_by_sku[sku]}; "
            f"used in assemblies: {assembled_by_sku[sku]}."
        )
    return created, updated


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
    purchased, sold_by_sku, assembled_by_sku, _, _ = await calculate_inventory_quantities(db)
    return InventoryListResponse(
        rows=[
            inventory_row(
                item,
                purchased_quantity=purchased.get(item.sku, {}).get("quantity", Decimal("0")),
                sold_quantity=sold_by_sku[item.sku],
                bundle_consumed_quantity=assembled_by_sku[item.sku],
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


@router.get("/opening-lots", response_model=OpeningLotListResponse)
async def list_opening_lots(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> OpeningLotListResponse:
    lots = await db.scalars(
        select(InventoryLot)
        .where(InventoryLot.source == "manual_opening")
        .order_by(InventoryLot.purchase_date, InventoryLot.id)
    )
    return OpeningLotListResponse(rows=[opening_lot_row(lot) for lot in lots])


@router.post("/opening-lots", response_model=OpeningLotRow)
async def create_opening_lot(
    payload: OpeningLotRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> OpeningLotRow:
    lot = InventoryLot(
        source="manual_opening",
        purchase_date=payload.purchase_date,
        sku=payload.sku.strip(),
        ean=clean_text(payload.ean),
        product_name=payload.product_name.strip(),
        quantity_received=Decimal(str(payload.quantity_received)),
        unit_cost=Decimal(str(payload.unit_cost)),
        currency=payload.currency.strip().upper(),
        notes=clean_text(payload.notes),
    )
    db.add(lot)
    await db.commit()
    await db.refresh(lot)
    return opening_lot_row(lot)


@router.delete("/opening-lots/{lot_id}")
async def delete_opening_lot(
    lot_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> dict[str, int | bool]:
    lot = await db.get(InventoryLot, lot_id)
    if lot is None or lot.source != "manual_opening":
        raise HTTPException(status_code=404, detail="Opening inventory lot was not found.")
    await db.delete(lot)
    await db.commit()
    return {"lot_id": lot_id, "deleted": True}


@router.get("/bundle-components", response_model=BundleComponentListResponse)
async def list_bundle_components(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> BundleComponentListResponse:
    components = await db.scalars(
        select(BundleComponent).order_by(
            BundleComponent.bundle_sku,
            BundleComponent.component_sku,
        )
    )
    return BundleComponentListResponse(
        rows=[bundle_component_row(component) for component in components]
    )


@router.get("/bundle-candidates", response_model=BundleCandidateResponse)
async def list_bundle_candidates(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> BundleCandidateResponse:
    order_rows = await db.execute(
        select(
            AmazonOrderItem.sku,
            AmazonOrderItem.product_name,
        )
        .where(AmazonOrderItem.sku != "")
        .where(AmazonOrderItem.quantity > 0)
        .order_by(AmazonOrderItem.sku, AmazonOrderItem.purchase_date.desc())
    )
    bundles_by_sku: dict[str, str | None] = {}
    for sku, product_name in order_rows:
        bundles_by_sku.setdefault(str(sku), product_name)

    lots = list(
        await db.scalars(
            select(InventoryLot).order_by(
                InventoryLot.purchase_date,
                InventoryLot.id,
            )
        )
    )
    components_by_sku: dict[str, dict[str, object]] = {}
    for lot in lots:
        sku = (lot.sku or lot.supplier_sku or lot.ean or "").strip()
        if not sku:
            continue
        bucket = components_by_sku.setdefault(
            sku,
            {
                "sku": sku,
                "product_name": lot.product_name,
                "available_quantity": 0.0,
                "latest_unit_cost": float(lot.unit_cost),
                "currency": lot.currency,
            },
        )
        bucket["available_quantity"] = (
            float(bucket["available_quantity"]) + float(lot.quantity_received)
        )
        bucket["product_name"] = lot.product_name
        bucket["latest_unit_cost"] = float(lot.unit_cost)
        bucket["currency"] = lot.currency

    return BundleCandidateResponse(
        bundles=[
            BundleCandidateRow(sku=sku, product_name=product_name)
            for sku, product_name in sorted(bundles_by_sku.items())
        ],
        components=[
            ComponentCandidateRow(**values)
            for values in components_by_sku.values()
        ],
    )


@router.post("/bundle-components", response_model=BundleComponentRow)
async def create_bundle_component(
    payload: BundleComponentRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> BundleComponentRow:
    bundle_sku = payload.bundle_sku.strip()
    component_sku = payload.component_sku.strip()
    existing = await db.scalar(
        select(BundleComponent).where(
            BundleComponent.bundle_sku == bundle_sku,
            BundleComponent.component_sku == component_sku,
        )
    )
    if existing:
        existing.component_quantity = Decimal(str(payload.component_quantity))
        existing.bundle_name = clean_text(payload.bundle_name)
        component = existing
    else:
        component = BundleComponent(
            bundle_sku=bundle_sku,
            bundle_name=clean_text(payload.bundle_name),
            component_sku=component_sku,
            component_quantity=Decimal(str(payload.component_quantity)),
        )
        db.add(component)
    await db.commit()
    await db.refresh(component)
    return bundle_component_row(component)


@router.post("/bundle-recipes", response_model=BundleComponentListResponse)
async def save_bundle_recipe(
    payload: BundleRecipeRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> BundleComponentListResponse:
    bundle_sku = payload.bundle_sku.strip()
    original_bundle_sku = clean_text(payload.original_bundle_sku)
    component_skus = [component.component_sku.strip() for component in payload.components]
    if len(component_skus) != len(set(component_skus)):
        raise HTTPException(status_code=422, detail="A component can appear only once in a bundle recipe.")

    skus_to_replace = {bundle_sku}
    if original_bundle_sku:
        skus_to_replace.add(original_bundle_sku)
    await db.execute(
        delete(BundleComponent).where(BundleComponent.bundle_sku.in_(skus_to_replace))
    )

    components = [
        BundleComponent(
            bundle_sku=bundle_sku,
            bundle_name=clean_text(payload.bundle_name),
            component_sku=component_sku,
            component_quantity=Decimal(str(component.component_quantity)),
        )
        for component, component_sku in zip(payload.components, component_skus, strict=True)
    ]
    db.add_all(components)
    await db.commit()
    for component in components:
        await db.refresh(component)
    return BundleComponentListResponse(
        rows=[bundle_component_row(component) for component in components]
    )


@router.delete("/bundle-components/{component_id}")
async def delete_bundle_component(
    component_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> dict[str, int | bool]:
    component = await db.get(BundleComponent, component_id)
    if component is None:
        raise HTTPException(status_code=404, detail="Bundle component was not found.")
    await db.delete(component)
    await db.commit()
    return {"component_id": component_id, "deleted": True}


@router.get("/bundle-assemblies", response_model=BundleAssemblyListResponse)
async def list_bundle_assemblies(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> BundleAssemblyListResponse:
    assemblies = await db.scalars(
        select(BundleAssembly).order_by(
            BundleAssembly.assembly_date.desc(),
            BundleAssembly.id.desc(),
        )
    )
    return BundleAssemblyListResponse(
        rows=[bundle_assembly_row(assembly) for assembly in assemblies]
    )


@router.post("/bundle-assemblies", response_model=BundleAssemblyRow)
async def create_bundle_assembly(
    payload: BundleAssemblyRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> BundleAssemblyRow:
    bundle_sku = payload.bundle_sku.strip()
    assembly_provider = normalize_assembly_provider(payload.assembly_provider)
    currency = payload.currency.strip().upper()
    recipe = list(
        await db.scalars(
            select(BundleComponent)
            .where(BundleComponent.bundle_sku == bundle_sku)
            .order_by(BundleComponent.component_sku)
        )
    )
    if not recipe:
        raise HTTPException(status_code=422, detail="Save the bundle recipe before recording assembly.")

    purchased, sold_by_sku, assembled_by_sku, _, _ = await calculate_inventory_quantities(db)
    required = bundle_component_sales(
        recipe,
        Decimal(str(payload.quantity)),
        purchased,
    )
    if required is None:
        raise HTTPException(status_code=422, detail="One or more bundle components have no inventory lot.")
    shortages = []
    for component_sku, required_quantity in required.items():
        available = (
            purchased[component_sku]["quantity"]
            - sold_by_sku[component_sku]
            - assembled_by_sku[component_sku]
        )
        if required_quantity > available:
            shortages.append(
                f"{component_sku}: required {required_quantity}, available {max(available, Decimal('0'))}"
            )
    if shortages:
        raise HTTPException(
            status_code=422,
            detail="Insufficient component inventory: " + "; ".join(shortages),
        )

    assembly = BundleAssembly(
        bundle_sku=bundle_sku,
        assembly_date=payload.assembly_date,
        quantity=Decimal(str(payload.quantity)),
        assembly_provider=assembly_provider,
        unit_assembly_cost=Decimal(str(payload.unit_assembly_cost)),
        currency=currency,
        component_snapshot=[
            {
                "component_sku": component.component_sku,
                "component_quantity": str(component.component_quantity),
            }
            for component in recipe
        ],
        notes=clean_text(payload.notes),
    )
    db.add(assembly)
    await db.commit()
    await db.refresh(assembly)
    purchased, sold_by_sku, assembled_by_sku, _, _ = await calculate_inventory_quantities(db)
    await update_estimated_inventory_items(db, purchased, sold_by_sku, assembled_by_sku)
    await db.commit()
    return bundle_assembly_row(assembly)


@router.put("/bundle-assemblies/{assembly_id}", response_model=BundleAssemblyRow)
async def update_bundle_assembly(
    assembly_id: int,
    payload: BundleAssemblyUpdateRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> BundleAssemblyRow:
    assembly = await db.get(BundleAssembly, assembly_id)
    if assembly is None:
        raise HTTPException(status_code=404, detail="Bundle assembly not found.")
    assembly.assembly_date = payload.assembly_date
    assembly.assembly_provider = normalize_assembly_provider(payload.assembly_provider)
    assembly.unit_assembly_cost = Decimal(str(payload.unit_assembly_cost))
    assembly.currency = payload.currency.strip().upper()
    assembly.notes = clean_text(payload.notes)
    await db.commit()
    await db.refresh(assembly)
    return bundle_assembly_row(assembly)


@router.delete("/bundle-assemblies/{assembly_id}")
async def delete_bundle_assembly(
    assembly_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> dict[str, int | bool]:
    assembly = await db.get(BundleAssembly, assembly_id)
    if assembly is None:
        raise HTTPException(status_code=404, detail="Bundle assembly not found.")
    await db.delete(assembly)
    await db.commit()
    purchased, sold_by_sku, assembled_by_sku, _, _ = await calculate_inventory_quantities(db)
    await update_estimated_inventory_items(db, purchased, sold_by_sku, assembled_by_sku)
    await db.commit()
    return {"assembly_id": assembly_id, "deleted": True}


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
    purchased, sold_by_sku, assembled_by_sku, _, _ = await calculate_inventory_quantities(db)
    return inventory_row(
        item,
        purchased_quantity=purchased.get(item.sku, {}).get("quantity", Decimal("0")),
        sold_quantity=sold_by_sku[item.sku],
        bundle_consumed_quantity=assembled_by_sku[item.sku],
    )


@router.post("/sync-from-invoices", response_model=SyncInventoryResponse)
async def sync_inventory_from_invoices(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> SyncInventoryResponse:
    purchased, sold_by_sku, assembled_by_sku, sales_matched, sales_unmatched = (
        await calculate_inventory_quantities(db)
    )

    created, updated = await update_estimated_inventory_items(
        db,
        purchased,
        sold_by_sku,
        assembled_by_sku,
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
    purchased, sold_by_sku, assembled_by_sku, _, _ = await calculate_inventory_quantities(db)
    return inventory_row(
        item,
        purchased_quantity=purchased.get(item.sku, {}).get("quantity", Decimal("0")),
        sold_quantity=sold_by_sku[item.sku],
        bundle_consumed_quantity=assembled_by_sku[item.sku],
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
