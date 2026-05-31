from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ingestion.generic_reports import GenericReportPreview, calculate_sha256
from app.models.generic_report_import import GenericReportImport
from app.models.generic_report_row import GenericReportRow
from app.services.amazon_payment_import_service import DuplicateImportError


async def commit_generic_report_import(
    db: AsyncSession,
    content: bytes,
    preview: GenericReportPreview,
) -> GenericReportImport:
    source_sha256 = calculate_sha256(content)
    existing = await db.scalar(
        select(GenericReportImport).where(GenericReportImport.source_sha256 == source_sha256)
    )
    if existing:
        raise DuplicateImportError(existing.id)

    report_import = GenericReportImport(
        report_type=preview.report_type,
        source_filename=preview.filename,
        source_sha256=source_sha256,
        row_count=preview.row_count,
    )
    db.add(report_import)
    await db.flush()

    for row_number, raw_row in enumerate(preview.raw_rows, start=2):
        db.add(
            GenericReportRow(
                import_id=report_import.id,
                row_number=row_number,
                raw_row=raw_row,
            )
        )

    await db.commit()
    await db.refresh(report_import)
    return report_import

