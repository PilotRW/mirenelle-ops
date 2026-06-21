from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Date, DateTime, Integer, Numeric, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class FbaStorageFee(Base):
    __tablename__ = "fba_storage_fees"
    __table_args__ = (
        UniqueConstraint(
            "month_of_charge",
            "fnsku",
            "fulfillment_center",
            "country_code",
            name="uq_fba_storage_fee_month_fnsku_center",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    month_of_charge: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    sku: Mapped[str | None] = mapped_column(String(160), nullable=True, index=True)
    fnsku: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    asin: Mapped[str | None] = mapped_column(String(32), nullable=True, index=True)
    product_name: Mapped[str | None] = mapped_column(Text, nullable=True)
    fulfillment_center: Mapped[str] = mapped_column(String(32), nullable=False)
    country_code: Mapped[str] = mapped_column(String(8), nullable=False)
    average_quantity_on_hand: Mapped[Decimal] = mapped_column(Numeric(12, 3), nullable=False)
    estimated_total_item_volume: Mapped[Decimal] = mapped_column(Numeric(16, 6), nullable=False)
    currency: Mapped[str] = mapped_column(String(8), nullable=False)
    estimated_monthly_storage_fee: Mapped[Decimal] = mapped_column(Numeric(12, 4), nullable=False)
    raw_row: Mapped[dict] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
