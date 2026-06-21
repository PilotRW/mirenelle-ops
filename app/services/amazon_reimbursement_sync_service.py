from datetime import date

import httpx
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.ingestion.amazon_reports.reimbursement_reports import (
    REPORT_TYPE_REIMBURSEMENTS,
    parse_reimbursements,
)
from app.models.amazon_reimbursement import AmazonReimbursement
from app.services.amazon_order_sync_service import _wait_for_report
from app.services.amazon_sp_api_client import AmazonSpApiClient, AmazonSpApiError


async def sync_reimbursements(
    db: AsyncSession,
    start_date: date,
    end_date: date,
) -> dict:
    sp_api = AmazonSpApiClient()
    async with httpx.AsyncClient(timeout=httpx.Timeout(120.0)) as client:
        report_id = await sp_api.create_report(
            client, "EU", REPORT_TYPE_REIMBURSEMENTS, start_date, end_date
        )
        try:
            report = await _wait_for_report(sp_api, client, report_id, 20, 600)
        except AmazonSpApiError:
            reports = await sp_api.get_reports(client, REPORT_TYPE_REIMBURSEMENTS, "EU")
            report = next((row for row in reports if row.get("reportDocumentId")), None)
            if report is None:
                raise
            report_id = str(report.get("reportId") or report_id)
        document_id = str(report.get("reportDocumentId") or "")
        if not document_id:
            raise AmazonSpApiError("Reimbursements report finished without a document.")
        content = await sp_api.download_document(
            client, await sp_api.get_report_document(client, document_id)
        )
    rows = parse_reimbursements(content)
    for values in rows:
        statement = insert(AmazonReimbursement).values(**values)
        statement = statement.on_conflict_do_update(
            index_elements=["reimbursement_id"],
            set_={key: getattr(statement.excluded, key) for key in values if key != "reimbursement_id"},
        )
        await db.execute(statement)
    await db.commit()
    return {
        "report_id": report_id,
        "report_document_id": document_id,
        "rows": len(rows),
        "amount_total": float(sum((row["amount_total"] for row in rows), start=0)),
        "processing_status": str(report.get("processingStatus") or ""),
    }
