import asyncio
from dataclasses import dataclass
from datetime import date, timedelta

import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from app.ingestion.amazon_reports.order_reports import build_order_report_preview
from app.models.amazon_order_import import AmazonOrderImport
from app.services.amazon_order_import_service import commit_order_report_import
from app.services.amazon_payment_import_service import DuplicateImportError
from app.services.amazon_sp_api_client import (
    DONE_REPORT_STATUSES,
    FAILED_REPORT_STATUSES,
    AmazonSpApiClient,
    AmazonSpApiError,
)


@dataclass(frozen=True)
class AmazonOrderSyncResult:
    status: str
    report_id: str | None
    report_document_id: str | None
    import_id: int | None
    report_ids: list[str]
    report_document_ids: list[str]
    import_ids: list[int]
    filename: str | None
    row_count: int
    fba_quantity: float
    fbm_quantity: float
    processing_status: str


async def sync_orders_report(
    db: AsyncSession,
    marketplace: str,
    start_date: date,
    end_date: date,
    poll_interval_seconds: int = 30,
    wait_timeout_seconds: int = 300,
) -> AmazonOrderSyncResult:
    results: list[AmazonOrderSyncResult] = []
    sp_api = AmazonSpApiClient()
    timeout = httpx.Timeout(connect=30.0, read=120.0, write=30.0, pool=30.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        for marketplace_code in _marketplace_codes(marketplace):
            for chunk_start, chunk_end in _date_chunks(start_date, end_date):
                results.append(
                    await _sync_orders_report_chunk(
                        db=db,
                        sp_api=sp_api,
                        client=client,
                        marketplace=marketplace_code,
                        start_date=chunk_start,
                        end_date=chunk_end,
                        poll_interval_seconds=poll_interval_seconds,
                        wait_timeout_seconds=wait_timeout_seconds,
                    )
                )
    return _merge_results(results)


async def _sync_orders_report_chunk(
    db: AsyncSession,
    sp_api: AmazonSpApiClient,
    client: httpx.AsyncClient,
    marketplace: str,
    start_date: date,
    end_date: date,
    poll_interval_seconds: int,
    wait_timeout_seconds: int,
) -> AmazonOrderSyncResult:
    report_id = await sp_api.create_orders_report(
        client=client,
        marketplace=marketplace,
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
    report_document_id = report.get("reportDocumentId")
    if not report_document_id:
        raise AmazonSpApiError(f"Report {report_id} finished without reportDocumentId.")

    document = await sp_api.get_report_document(client, str(report_document_id))
    content = await sp_api.download_document(client, document)

    filename = f"amazon-orders-{marketplace.upper()}-{start_date.isoformat()}-{end_date.isoformat()}-{report_id}.tsv"
    preview = build_order_report_preview(
        filename=filename,
        content=content,
        marketplace=marketplace.upper(),
    )
    if not preview.can_commit:
        raise AmazonSpApiError(
            "Downloaded order report cannot be imported: "
            f"missing_fields={preview.missing_fields}, validation_errors={preview.validation_errors[:5]}"
        )

    try:
        order_import = await commit_order_report_import(
            db=db,
            marketplace=marketplace.upper(),
            content=content,
            preview=preview,
        )
    except DuplicateImportError as exc:
        return AmazonOrderSyncResult(
            status="duplicate",
            report_id=report_id,
            report_document_id=str(report_document_id),
            import_id=exc.import_id,
            report_ids=[report_id],
            report_document_ids=[str(report_document_id)],
            import_ids=[exc.import_id],
            filename=filename,
            row_count=preview.row_count,
            fba_quantity=float(preview.totals.get("fba_quantity", 0)),
            fbm_quantity=float(preview.totals.get("fbm_quantity", 0)),
            processing_status=str(report.get("processingStatus") or ""),
        )

    return _result_from_import(
        order_import=order_import,
        report_id=report_id,
        report_document_id=str(report_document_id),
        preview=preview,
        processing_status=str(report.get("processingStatus") or ""),
    )


async def _wait_for_report(
    sp_api: AmazonSpApiClient,
    client: httpx.AsyncClient,
    report_id: str,
    poll_interval_seconds: int,
    wait_timeout_seconds: int,
) -> dict:
    elapsed = 0
    interval = max(10, poll_interval_seconds)
    timeout = max(interval, wait_timeout_seconds)
    while elapsed <= timeout:
        report = await sp_api.get_report(client, report_id)
        status = str(report.get("processingStatus") or "")
        if status in DONE_REPORT_STATUSES:
            return report
        if status in FAILED_REPORT_STATUSES:
            raise AmazonSpApiError(f"Report {report_id} finished with status {status}.")
        await asyncio.sleep(interval)
        elapsed += interval
    raise AmazonSpApiError(f"Report {report_id} was not ready after {timeout} seconds.")


def _date_chunks(start_date: date, end_date: date) -> list[tuple[date, date]]:
    chunks: list[tuple[date, date]] = []
    current = start_date
    while current <= end_date:
        chunk_end = min(current + timedelta(days=29), end_date)
        chunks.append((current, chunk_end))
        current = chunk_end + timedelta(days=1)
    return chunks


def _marketplace_codes(marketplace: str) -> tuple[str, ...]:
    normalized = marketplace.upper()
    if normalized == "EU":
        return ("EU",)
    return (normalized,)


def _merge_results(results: list[AmazonOrderSyncResult]) -> AmazonOrderSyncResult:
    if not results:
        raise AmazonSpApiError("No report chunks were requested.")
    report_ids = [report_id for result in results for report_id in result.report_ids]
    report_document_ids = [document_id for result in results for document_id in result.report_document_ids]
    import_ids = [import_id for result in results for import_id in result.import_ids]
    status = "duplicate" if all(result.status == "duplicate" for result in results) else "imported"
    return AmazonOrderSyncResult(
        status=status,
        report_id=report_ids[0] if len(report_ids) == 1 else None,
        report_document_id=report_document_ids[0] if len(report_document_ids) == 1 else None,
        import_id=import_ids[0] if len(import_ids) == 1 else None,
        report_ids=report_ids,
        report_document_ids=report_document_ids,
        import_ids=import_ids,
        filename=", ".join(result.filename or "-" for result in results),
        row_count=sum(result.row_count for result in results),
        fba_quantity=sum(result.fba_quantity for result in results),
        fbm_quantity=sum(result.fbm_quantity for result in results),
        processing_status=", ".join(result.processing_status for result in results),
    )


def _result_from_import(
    order_import: AmazonOrderImport,
    report_id: str,
    report_document_id: str,
    preview,
    processing_status: str,
) -> AmazonOrderSyncResult:
    return AmazonOrderSyncResult(
        status="imported",
        report_id=report_id,
        report_document_id=report_document_id,
        import_id=order_import.id,
        report_ids=[report_id],
        report_document_ids=[report_document_id],
        import_ids=[order_import.id],
        filename=order_import.source_filename,
        row_count=order_import.row_count,
        fba_quantity=float(preview.totals.get("fba_quantity", 0)),
        fbm_quantity=float(preview.totals.get("fbm_quantity", 0)),
        processing_status=processing_status,
    )
