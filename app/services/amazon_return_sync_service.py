from dataclasses import dataclass
from datetime import date

import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from app.ingestion.amazon_reports.return_reports import (
    REPORT_TYPE_CUSTOMER_RETURNS,
    build_return_report_preview,
)
from app.services.amazon_order_sync_service import _wait_for_report
from app.services.amazon_payment_import_service import DuplicateImportError
from app.services.amazon_return_import_service import commit_return_report_import
from app.services.amazon_sp_api_client import AmazonSpApiClient, AmazonSpApiError


@dataclass(frozen=True)
class AmazonReturnSyncResult:
    status: str
    report_id: str
    report_document_id: str
    import_id: int
    filename: str
    row_count: int
    processing_status: str


async def sync_returns_report(
    db: AsyncSession,
    marketplace: str,
    start_date: date,
    end_date: date,
    poll_interval_seconds: int = 30,
    wait_timeout_seconds: int = 600,
) -> AmazonReturnSyncResult:
    sp_api = AmazonSpApiClient()
    async with httpx.AsyncClient(timeout=httpx.Timeout(120.0)) as client:
        report_id = await sp_api.create_report(
            client=client,
            marketplace=marketplace,
            report_type=REPORT_TYPE_CUSTOMER_RETURNS,
            start_date=start_date,
            end_date=end_date,
        )
        report = await _wait_for_report(
            sp_api=sp_api,
            client=client,
            report_id=report_id,
            poll_interval_seconds=poll_interval_seconds,
            wait_timeout_seconds=wait_timeout_seconds,
        )
        document_id = str(report.get("reportDocumentId") or "")
        if not document_id:
            raise AmazonSpApiError(f"Return report {report_id} finished without reportDocumentId.")
        document = await sp_api.get_report_document(client, document_id)
        content = await sp_api.download_document(client, document)

    filename = f"amazon-returns-{marketplace.upper()}-{start_date.isoformat()}-{end_date.isoformat()}-{report_id}.tsv"
    preview = build_return_report_preview(filename, content, marketplace.upper())
    if not preview.can_commit:
        raise AmazonSpApiError(
            "Downloaded returns report cannot be imported: "
            f"missing_fields={preview.missing_fields}, validation_errors={preview.validation_errors[:5]}"
        )
    try:
        report_import = await commit_return_report_import(
            db=db,
            marketplace=marketplace.upper(),
            content=content,
            preview=preview,
        )
        status = "imported"
        import_id = report_import.id
    except DuplicateImportError as exc:
        status = "duplicate"
        import_id = exc.import_id
    return AmazonReturnSyncResult(
        status=status,
        report_id=report_id,
        report_document_id=document_id,
        import_id=import_id,
        filename=filename,
        row_count=preview.row_count,
        processing_status=str(report.get("processingStatus") or ""),
    )
