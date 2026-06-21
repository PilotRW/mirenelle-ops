from datetime import datetime

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class AmazonReturnImport(Base):
    __tablename__ = "amazon_return_imports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    source_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    source_sha256: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    marketplace: Mapped[str] = mapped_column(String(16), nullable=False, index=True)
    report_type: Mapped[str] = mapped_column(String(120), nullable=False)
    report_period_start: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    report_period_end: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    header_mapping: Mapped[dict] = mapped_column(JSONB, nullable=False)
    row_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )
