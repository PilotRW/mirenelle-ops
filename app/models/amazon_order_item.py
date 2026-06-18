from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class AmazonOrderItem(Base):
    __tablename__ = "amazon_order_items"
    __table_args__ = (
        UniqueConstraint(
            "amazon_order_id",
            "sku",
            "asin",
            name="uq_amazon_order_items_order_sku_asin",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    import_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("amazon_order_imports.id"),
        nullable=False,
        index=True,
    )
    marketplace: Mapped[str] = mapped_column(String(16), nullable=False, index=True)
    amazon_order_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    merchant_order_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    purchase_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, index=True)
    last_updated_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    order_status: Mapped[str | None] = mapped_column(String(80), nullable=True, index=True)
    item_status: Mapped[str | None] = mapped_column(String(80), nullable=True, index=True)
    fulfillment_channel: Mapped[str] = mapped_column(String(16), nullable=False, index=True)
    sales_channel: Mapped[str | None] = mapped_column(String(80), nullable=True)
    ship_service_level: Mapped[str | None] = mapped_column(String(120), nullable=True)
    sku: Mapped[str] = mapped_column(String(160), nullable=False, index=True)
    asin: Mapped[str | None] = mapped_column(String(32), nullable=True, index=True)
    product_name: Mapped[str | None] = mapped_column(Text, nullable=True)
    quantity: Mapped[Decimal] = mapped_column(Numeric(12, 3), nullable=False)
    currency: Mapped[str | None] = mapped_column(String(8), nullable=True, index=True)
    item_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    item_tax: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    shipping_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    shipping_tax: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    item_promotion_discount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    ship_promotion_discount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    raw_row: Mapped[dict] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )
