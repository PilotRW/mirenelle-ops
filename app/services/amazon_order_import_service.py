from datetime import datetime
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.ingestion.amazon_reports.order_reports import (
    OrderReportPreview,
    REPORT_TYPE_ALL_ORDERS_BY_ORDER_DATE,
    calculate_sha256,
)
from app.models.amazon_order_import import AmazonOrderImport
from app.models.amazon_order_item import AmazonOrderItem
from app.services.amazon_payment_import_service import DuplicateImportError


def _period_bounds(preview: OrderReportPreview) -> tuple[datetime | None, datetime | None]:
    dates = [row["purchase_date"] for row in preview.parsed_rows if row.get("purchase_date")]
    if not dates:
        return None, None
    return min(dates), max(dates)


async def commit_order_report_import(
    db: AsyncSession,
    marketplace: str,
    content: bytes,
    preview: OrderReportPreview,
) -> AmazonOrderImport:
    source_sha256 = calculate_sha256(content)
    existing = await db.scalar(
        select(AmazonOrderImport).where(AmazonOrderImport.source_sha256 == source_sha256)
    )
    if existing:
        raise DuplicateImportError(existing.id)

    period_start, period_end = _period_bounds(preview)
    order_import = AmazonOrderImport(
        source_filename=preview.filename,
        source_sha256=source_sha256,
        marketplace=marketplace,
        report_type=REPORT_TYPE_ALL_ORDERS_BY_ORDER_DATE,
        report_period_start=period_start,
        report_period_end=period_end,
        header_mapping=preview.mapping,
        row_count=preview.row_count,
    )
    db.add(order_import)
    await db.flush()

    for parsed in preview.parsed_rows:
        values = {
            "import_id": order_import.id,
            "marketplace": str(parsed["marketplace"]),
            "amazon_order_id": str(parsed["amazon_order_id"]),
            "merchant_order_id": parsed["merchant_order_id"],
            "purchase_date": parsed["purchase_date"],
            "last_updated_date": parsed["last_updated_date"],
            "order_status": parsed["order_status"],
            "item_status": parsed["item_status"],
            "fulfillment_channel": str(parsed["fulfillment_channel"]),
            "sales_channel": parsed["sales_channel"],
            "ship_service_level": parsed["ship_service_level"],
            "sku": str(parsed["sku"]),
            "asin": parsed["asin"],
            "product_name": parsed["product_name"],
            "quantity": parsed["quantity"] if isinstance(parsed["quantity"], Decimal) else Decimal("0"),
            "currency": parsed["currency"],
            "item_price": parsed["item_price"] if isinstance(parsed["item_price"], Decimal) else Decimal("0"),
            "item_tax": parsed["item_tax"] if isinstance(parsed["item_tax"], Decimal) else Decimal("0"),
            "shipping_price": parsed["shipping_price"] if isinstance(parsed["shipping_price"], Decimal) else Decimal("0"),
            "shipping_tax": parsed["shipping_tax"] if isinstance(parsed["shipping_tax"], Decimal) else Decimal("0"),
            "item_promotion_discount": parsed["item_promotion_discount"] if isinstance(parsed["item_promotion_discount"], Decimal) else Decimal("0"),
            "ship_promotion_discount": parsed["ship_promotion_discount"] if isinstance(parsed["ship_promotion_discount"], Decimal) else Decimal("0"),
            "raw_row": parsed["raw_row"],
        }
        statement = insert(AmazonOrderItem).values(**values)
        statement = statement.on_conflict_do_update(
            constraint="uq_amazon_order_items_order_sku_asin",
            set_={
                key: getattr(statement.excluded, key)
                for key in values
                if key not in {"amazon_order_id", "sku", "asin"}
            },
        )
        await db.execute(statement)

    await db.commit()
    await db.refresh(order_import)
    return order_import
