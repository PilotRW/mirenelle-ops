from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Integer, Numeric, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class InventoryItem(Base):
    __tablename__ = "inventory_items"
    __table_args__ = (
        UniqueConstraint(
            "sku",
            "marketplace",
            "fulfillment_channel",
            name="uq_inventory_items_sku_marketplace_channel",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sku: Mapped[str] = mapped_column(String(160), nullable=False, index=True)
    ean: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    asin: Mapped[str | None] = mapped_column(String(32), nullable=True, index=True)
    product_name: Mapped[str | None] = mapped_column(Text, nullable=True)
    marketplace: Mapped[str] = mapped_column(String(16), nullable=False, default="EU", index=True)
    fulfillment_channel: Mapped[str] = mapped_column(String(40), nullable=False, default="FBA", index=True)
    quantity_on_hand: Mapped[Decimal] = mapped_column(Numeric(12, 3), nullable=False, default=0)
    quantity_reserved: Mapped[Decimal] = mapped_column(Numeric(12, 3), nullable=False, default=0)
    quantity_inbound: Mapped[Decimal] = mapped_column(Numeric(12, 3), nullable=False, default=0)
    reorder_point: Mapped[Decimal] = mapped_column(Numeric(12, 3), nullable=False, default=0)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
