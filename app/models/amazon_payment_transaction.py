from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Date, DateTime, ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class AmazonPaymentTransaction(Base):
    __tablename__ = "amazon_payment_transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    import_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("amazon_payment_imports.id"),
        nullable=False,
        index=True,
    )
    raw_row_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("amazon_payment_transaction_raw.id"),
        nullable=False,
        index=True,
    )
    marketplace: Mapped[str] = mapped_column(String(16), nullable=False, index=True)
    currency: Mapped[str] = mapped_column(String(8), nullable=False, index=True)
    transaction_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    transaction_status: Mapped[str] = mapped_column(String(120), nullable=False)
    transaction_type: Mapped[str] = mapped_column(String(160), nullable=False, index=True)
    external_transaction_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    sku: Mapped[str | None] = mapped_column(String(160), nullable=True, index=True)
    quantity: Mapped[Decimal | None] = mapped_column(Numeric(12, 3), nullable=True)
    product_details: Mapped[str | None] = mapped_column(Text, nullable=True)
    product_charges: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    promotional_rebates: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    amazon_fees: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    other_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    total_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    raw_row: Mapped[dict] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )
