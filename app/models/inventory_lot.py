from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Date, DateTime, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class InventoryLot(Base):
    __tablename__ = "inventory_lots"
    __table_args__ = (
        UniqueConstraint("invoice_line_id", name="uq_inventory_lots_invoice_line"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    invoice_line_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("purchase_invoice_lines.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    product_cost_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("product_costs.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    source: Mapped[str] = mapped_column(String(40), nullable=False, default="purchase_invoice", index=True)
    purchase_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    supplier_sku: Mapped[str | None] = mapped_column(String(120), nullable=True, index=True)
    sku: Mapped[str | None] = mapped_column(String(120), nullable=True, index=True)
    ean: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    product_name: Mapped[str] = mapped_column(Text, nullable=False)
    quantity_received: Mapped[Decimal] = mapped_column(Numeric(12, 3), nullable=False)
    unit_cost: Mapped[Decimal] = mapped_column(Numeric(12, 4), nullable=False)
    currency: Mapped[str] = mapped_column(String(8), nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )
