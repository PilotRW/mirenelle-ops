from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Integer, Numeric, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class BundleComponent(Base):
    __tablename__ = "bundle_components"
    __table_args__ = (
        UniqueConstraint(
            "bundle_sku",
            "component_sku",
            name="uq_bundle_components_bundle_component",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    bundle_sku: Mapped[str] = mapped_column(String(160), nullable=False, index=True)
    bundle_name: Mapped[str | None] = mapped_column(String(500), nullable=True)
    component_sku: Mapped[str] = mapped_column(String(160), nullable=False, index=True)
    component_quantity: Mapped[Decimal] = mapped_column(Numeric(12, 3), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )
