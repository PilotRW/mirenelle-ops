from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.ingestion.amazon_reports.return_reports import (
    REPORT_TYPE_CUSTOMER_RETURNS,
    ReturnReportPreview,
    calculate_sha256,
)
from app.models.amazon_return_import import AmazonReturnImport
from app.models.amazon_return_item import AmazonReturnItem
from app.services.amazon_payment_import_service import DuplicateImportError


async def commit_return_report_import(
    db: AsyncSession,
    marketplace: str,
    content: bytes,
    preview: ReturnReportPreview,
) -> AmazonReturnImport:
    source_sha256 = calculate_sha256(content)
    existing = await db.scalar(
        select(AmazonReturnImport).where(AmazonReturnImport.source_sha256 == source_sha256)
    )
    if existing:
        raise DuplicateImportError(existing.id)

    dates = [row["return_date"] for row in preview.parsed_rows]
    report_import = AmazonReturnImport(
        source_filename=preview.filename,
        source_sha256=source_sha256,
        marketplace=marketplace,
        report_type=REPORT_TYPE_CUSTOMER_RETURNS,
        report_period_start=min(dates) if dates else None,
        report_period_end=max(dates) if dates else None,
        header_mapping=preview.mapping,
        row_count=preview.row_count,
    )
    db.add(report_import)
    await db.flush()

    for parsed in preview.parsed_rows:
        values = dict(parsed)
        values["import_id"] = report_import.id
        statement = insert(AmazonReturnItem).values(**values)
        statement = statement.on_conflict_do_update(
            constraint="uq_amazon_return_items_order_fnsku_date_lpn",
            set_={
                key: getattr(statement.excluded, key)
                for key in values
                if key not in {"order_id", "fnsku", "return_date", "license_plate_number"}
            },
        )
        await db.execute(statement)

    await db.commit()
    await db.refresh(report_import)
    return report_import
