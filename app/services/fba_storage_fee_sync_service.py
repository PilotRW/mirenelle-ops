from datetime import date

import httpx
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.ingestion.amazon_reports.storage_fee_reports import (
    REPORT_TYPE_STORAGE_FEES,
    parse_storage_fees,
)
from app.models.fba_inventory_snapshot import FbaInventorySnapshot
from app.models.fba_storage_fee import FbaStorageFee
from app.services.amazon_order_sync_service import _wait_for_report
from app.services.amazon_sp_api_client import AmazonSpApiClient, AmazonSpApiError


async def sync_storage_fees(db: AsyncSession, month: date) -> dict:
    sp_api = AmazonSpApiClient()
    async with httpx.AsyncClient(timeout=httpx.Timeout(120.0)) as client:
        report_id = await sp_api.create_report(
            client, "EU", REPORT_TYPE_STORAGE_FEES, month, month
        )
        try:
            report = await _wait_for_report(sp_api, client, report_id, 20, 600)
        except AmazonSpApiError:
            reports = await sp_api.get_reports(client, REPORT_TYPE_STORAGE_FEES, "EU")
            report = next((row for row in reports if row.get("reportDocumentId")), None)
            if report is None:
                raise
            report_id = str(report.get("reportId") or report_id)
        document_id = str(report.get("reportDocumentId") or "")
        content = await sp_api.download_document(
            client, await sp_api.get_report_document(client, document_id)
        )
    snapshots = list(
        await db.scalars(
            select(FbaInventorySnapshot).order_by(FbaInventorySnapshot.captured_at.desc())
        )
    )
    sku_by_fnsku: dict[str, str] = {}
    for snapshot in snapshots:
        sku_by_fnsku.setdefault(snapshot.fnsku, snapshot.sku)
    rows = parse_storage_fees(content, sku_by_fnsku)
    for values in rows:
        statement = insert(FbaStorageFee).values(**values)
        statement = statement.on_conflict_do_update(
            constraint="uq_fba_storage_fee_month_fnsku_center",
            set_={
                key: getattr(statement.excluded, key)
                for key in values
                if key not in {"month_of_charge", "fnsku", "fulfillment_center", "country_code"}
            },
        )
        await db.execute(statement)
    await db.commit()
    return {
        "report_id": report_id,
        "report_document_id": document_id,
        "rows": len(rows),
        "mapped_rows": sum(1 for row in rows if row["sku"]),
        "amount_total": float(sum((row["estimated_monthly_storage_fee"] for row in rows), start=0)),
        "processing_status": str(report.get("processingStatus") or ""),
    }
