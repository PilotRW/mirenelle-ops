from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class ProductMapping(Base):
    __tablename__ = "product_mappings"
    __table_args__ = (
        UniqueConstraint(
            "invoice_line_id",
            "amazon_product_details",
            name="uq_product_mappings_invoice_line_amazon_product",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    invoice_line_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("purchase_invoice_lines.id"),
        nullable=False,
        index=True,
    )
    amazon_product_details: Mapped[str] = mapped_column(Text, nullable=False, index=True)
    supplier_name: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    supplier_sku: Mapped[str | None] = mapped_column(String(120), nullable=True, index=True)
    sku: Mapped[str | None] = mapped_column(String(120), nullable=True, index=True)
    ean: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    invoice_product_name: Mapped[str] = mapped_column(Text, nullable=False)
    confidence: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    match_method: Mapped[str] = mapped_column(String(40), nullable=False, default="manual")
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    raw_match: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )
