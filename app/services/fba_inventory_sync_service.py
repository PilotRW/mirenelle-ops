from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal

import httpx
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.ingestion.amazon_reports.fba_inventory_reports import (
    REPORT_TYPE_FBA_INVENTORY,
    parse_fba_inventory_report,
)
from app.models.fba_inventory_snapshot import FbaInventorySnapshot
from app.models.inventory_item import InventoryItem
from app.services.amazon_order_sync_service import _wait_for_report
from app.services.amazon_sp_api_client import AmazonSpApiClient, AmazonSpApiError


@dataclass(frozen=True)
class FbaInventorySyncResult:
    report_id: str
    report_document_id: str
    captured_at: str
    rows: int
    fulfillable_quantity: float
    reserved_quantity: float
    inbound_quantity: float
    processing_status: str


async def sync_fba_inventory(
    db: AsyncSession,
    marketplace: str = "EU",
    poll_interval_seconds: int = 20,
    wait_timeout_seconds: int = 600,
) -> FbaInventorySyncResult:
    captured_at = datetime.utcnow().replace(microsecond=0)
    sp_api = AmazonSpApiClient()
    async with httpx.AsyncClient(timeout=httpx.Timeout(120.0)) as client:
        report_id = await sp_api.create_report(
            client=client,
            marketplace=marketplace,
            report_type=REPORT_TYPE_FBA_INVENTORY,
            start_date=date.today(),
            end_date=date.today(),
        )
        try:
            report = await _wait_for_report(
                sp_api=sp_api,
                client=client,
                report_id=report_id,
                poll_interval_seconds=poll_interval_seconds,
                wait_timeout_seconds=wait_timeout_seconds,
            )
        except AmazonSpApiError:
            completed = await sp_api.get_reports(
                client=client,
                report_type=REPORT_TYPE_FBA_INVENTORY,
                marketplace=marketplace,
            )
            report = next(
                (candidate for candidate in completed if candidate.get("reportDocumentId")),
                None,
            )
            if report is None:
                raise
            report_id = str(report.get("reportId") or report_id)
        document_id = str(report.get("reportDocumentId") or "")
        if not document_id:
            raise AmazonSpApiError(f"FBA inventory report {report_id} finished without reportDocumentId.")
        document = await sp_api.get_report_document(client, document_id)
        content = await sp_api.download_document(client, document)

    rows = parse_fba_inventory_report(content, marketplace.upper(), captured_at)
    for values in rows:
        await db.execute(insert(FbaInventorySnapshot).values(**values))
        item = await db.scalar(
            select(InventoryItem)
            .where(InventoryItem.sku == values["sku"])
            .where(InventoryItem.marketplace == marketplace.upper())
            .where(InventoryItem.fulfillment_channel == "FBA")
        )
        if item is None:
            item = InventoryItem(
                sku=values["sku"],
                marketplace=marketplace.upper(),
                fulfillment_channel="FBA",
            )
            db.add(item)
        fulfillable = Decimal(str(values["fulfillable_quantity"]))
        reserved = Decimal(str(values["reserved_quantity"]))
        inbound = (
            Decimal(str(values["inbound_working_quantity"]))
            + Decimal(str(values["inbound_shipped_quantity"]))
            + Decimal(str(values["inbound_receiving_quantity"]))
        )
        item.asin = values["asin"]
        item.product_name = values["product_name"]
        item.quantity_on_hand = fulfillable + reserved
        item.quantity_reserved = reserved
        item.quantity_inbound = inbound
        item.notes = (
            f"FBA snapshot {captured_at.isoformat()}; "
            f"fulfillable={fulfillable}; reserved={reserved}; inbound={inbound}; "
            f"unsellable={values['unsellable_quantity']}."
        )
    await db.commit()
    return FbaInventorySyncResult(
        report_id=report_id,
        report_document_id=document_id,
        captured_at=captured_at.isoformat(),
        rows=len(rows),
        fulfillable_quantity=float(sum((row["fulfillable_quantity"] for row in rows), Decimal("0"))),
        reserved_quantity=float(sum((row["reserved_quantity"] for row in rows), Decimal("0"))),
        inbound_quantity=float(
            sum(
                (
                    row["inbound_working_quantity"]
                    + row["inbound_shipped_quantity"]
                    + row["inbound_receiving_quantity"]
                    for row in rows
                ),
                Decimal("0"),
            )
        ),
        processing_status=str(report.get("processingStatus") or ""),
    )
