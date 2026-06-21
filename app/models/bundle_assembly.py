from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Date, DateTime, Integer, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class BundleAssembly(Base):
    __tablename__ = "bundle_assemblies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    bundle_sku: Mapped[str] = mapped_column(String(160), nullable=False, index=True)
    assembly_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    quantity: Mapped[Decimal] = mapped_column(Numeric(12, 3), nullable=False)
    assembly_provider: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        server_default="unknown",
    )
    unit_assembly_cost: Mapped[Decimal] = mapped_column(
        Numeric(12, 4),
        nullable=False,
        server_default="0",
    )
    currency: Mapped[str] = mapped_column(
        String(8),
        nullable=False,
        server_default="EUR",
    )
    component_snapshot: Mapped[list[dict]] = mapped_column(JSONB, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )
