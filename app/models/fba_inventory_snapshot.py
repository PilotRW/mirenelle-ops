from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Integer, Numeric, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class FbaInventorySnapshot(Base):
    __tablename__ = "fba_inventory_snapshots"
    __table_args__ = (
        UniqueConstraint("captured_at", "sku", "fnsku", name="uq_fba_inventory_snapshot_sku"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    captured_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    marketplace: Mapped[str] = mapped_column(String(16), nullable=False, index=True)
    sku: Mapped[str] = mapped_column(String(160), nullable=False, index=True)
    fnsku: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    asin: Mapped[str | None] = mapped_column(String(32), nullable=True, index=True)
    product_name: Mapped[str | None] = mapped_column(Text, nullable=True)
    condition: Mapped[str | None] = mapped_column(String(40), nullable=True)
    fulfillable_quantity: Mapped[Decimal] = mapped_column(Numeric(12, 3), nullable=False)
    warehouse_quantity: Mapped[Decimal] = mapped_column(Numeric(12, 3), nullable=False)
    unsellable_quantity: Mapped[Decimal] = mapped_column(Numeric(12, 3), nullable=False)
    reserved_quantity: Mapped[Decimal] = mapped_column(Numeric(12, 3), nullable=False)
    total_quantity: Mapped[Decimal] = mapped_column(Numeric(12, 3), nullable=False)
    inbound_working_quantity: Mapped[Decimal] = mapped_column(Numeric(12, 3), nullable=False)
    inbound_shipped_quantity: Mapped[Decimal] = mapped_column(Numeric(12, 3), nullable=False)
    inbound_receiving_quantity: Mapped[Decimal] = mapped_column(Numeric(12, 3), nullable=False)
    researching_quantity: Mapped[Decimal] = mapped_column(Numeric(12, 3), nullable=False)
    raw_row: Mapped[dict] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
