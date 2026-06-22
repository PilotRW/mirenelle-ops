from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class ProductPrepCost(Base):
    __tablename__ = "product_prep_costs"

    sku: Mapped[str] = mapped_column(String(120), primary_key=True)
    fba_prep_per_unit: Mapped[Decimal] = mapped_column(
        Numeric(12, 4),
        nullable=False,
        default=0,
    )
    fbm_prep_per_unit: Mapped[Decimal] = mapped_column(
        Numeric(12, 4),
        nullable=False,
        default=0,
    )
    currency: Mapped[str] = mapped_column(String(8), nullable=False, default="EUR")
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
