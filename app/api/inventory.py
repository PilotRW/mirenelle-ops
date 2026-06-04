from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.models.inventory_item import InventoryItem


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


def clean_text(value: str | None) -> str | None:
    return (value or "").strip() or None


def inventory_status(item: InventoryItem) -> str:
    available = (item.quantity_on_hand or Decimal("0")) - (item.quantity_reserved or Decimal("0"))
    if available <= 0:
        return "out_of_stock"
    if item.reorder_point and available <= item.reorder_point:
        return "low_stock"
    return "healthy"


def inventory_row(item: InventoryItem) -> InventoryItemRow:
    available = (item.quantity_on_hand or Decimal("0")) - (item.quantity_reserved or Decimal("0"))
    return InventoryItemRow(
        id=item.id,
        sku=item.sku,
        ean=item.ean,
        asin=item.asin,
        product_name=item.product_name,
        marketplace=item.marketplace,
        fulfillment_channel=item.fulfillment_channel,
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
    return InventoryListResponse(rows=[inventory_row(item) for item in result])


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
    return inventory_row(item)


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
    return inventory_row(item)


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
