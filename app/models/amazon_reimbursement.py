from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Integer, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class AmazonReimbursement(Base):
    __tablename__ = "amazon_reimbursements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reimbursement_id: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    approval_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    amazon_order_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    reason: Mapped[str | None] = mapped_column(String(120), nullable=True)
    sku: Mapped[str] = mapped_column(String(160), nullable=False, index=True)
    fnsku: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    asin: Mapped[str | None] = mapped_column(String(32), nullable=True, index=True)
    product_name: Mapped[str | None] = mapped_column(Text, nullable=True)
    currency: Mapped[str] = mapped_column(String(8), nullable=False)
    amount_total: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    quantity_cash: Mapped[Decimal] = mapped_column(Numeric(12, 3), nullable=False)
    quantity_inventory: Mapped[Decimal] = mapped_column(Numeric(12, 3), nullable=False)
    quantity_total: Mapped[Decimal] = mapped_column(Numeric(12, 3), nullable=False)
    raw_row: Mapped[dict] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
