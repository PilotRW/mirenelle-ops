from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class AmazonReturnItem(Base):
    __tablename__ = "amazon_return_items"
    __table_args__ = (
        UniqueConstraint(
            "order_id",
            "fnsku",
            "return_date",
            "license_plate_number",
            name="uq_amazon_return_items_order_fnsku_date_lpn",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    import_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("amazon_return_imports.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    marketplace: Mapped[str] = mapped_column(String(16), nullable=False, index=True)
    return_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    order_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    sku: Mapped[str] = mapped_column(String(160), nullable=False, index=True)
    asin: Mapped[str | None] = mapped_column(String(32), nullable=True, index=True)
    fnsku: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    product_name: Mapped[str | None] = mapped_column(Text, nullable=True)
    quantity: Mapped[Decimal] = mapped_column(Numeric(12, 3), nullable=False)
    fulfillment_center_id: Mapped[str | None] = mapped_column(String(32), nullable=True)
    detailed_disposition: Mapped[str | None] = mapped_column(String(80), nullable=True)
    reason: Mapped[str | None] = mapped_column(String(120), nullable=True)
    status: Mapped[str | None] = mapped_column(String(160), nullable=True)
    license_plate_number: Mapped[str] = mapped_column(String(120), nullable=False, default="")
    customer_comments: Mapped[str | None] = mapped_column(Text, nullable=True)
    raw_row: Mapped[dict] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )
