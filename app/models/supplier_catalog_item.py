from datetime import datetime
from decimal import Decimal

from sqlalchemy import BigInteger, DateTime, Integer, Numeric, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class SupplierCatalogItem(Base):
    __tablename__ = "supplier_catalog_items"
    __table_args__ = (
        UniqueConstraint("source", "source_offer_id", name="uq_supplier_catalog_items_source_offer"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    source: Mapped[str] = mapped_column(String(40), nullable=False, default="oa_pipeline", index=True)
    source_offer_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True)
    supplier_name: Mapped[str | None] = mapped_column(Text, nullable=True, index=True)
    supplier_sku: Mapped[str | None] = mapped_column(String(160), nullable=True, index=True)
    ean: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    brand: Mapped[str | None] = mapped_column(Text, nullable=True)
    title: Mapped[str | None] = mapped_column(Text, nullable=True)
    cost: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    currency: Mapped[str | None] = mapped_column(String(8), nullable=True)
    source_imported_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    raw_data: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    synced_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
