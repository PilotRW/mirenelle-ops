from datetime import datetime
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ingestion.amazon_reports.payment_transactions import (
    PaymentTransactionPreview,
    calculate_sha256,
)
from app.models.amazon_payment_import import AmazonPaymentImport
from app.models.amazon_payment_transaction import AmazonPaymentTransaction
from app.models.amazon_payment_transaction_raw import AmazonPaymentTransactionRaw


class DuplicateImportError(Exception):
    def __init__(self, import_id: int) -> None:
        self.import_id = import_id
        super().__init__(f"File already imported as import {import_id}.")


def _period_bounds(preview: PaymentTransactionPreview) -> tuple[datetime | None, datetime | None]:
    dates = [row["transaction_date"] for row in preview.parsed_rows if row.get("transaction_date")]
    if not dates:
        return None, None
    return (
        datetime.combine(min(dates), datetime.min.time()),
        datetime.combine(max(dates), datetime.min.time()),
    )


async def commit_payment_transaction_import(
    db: AsyncSession,
    marketplace: str,
    content: bytes,
    preview: PaymentTransactionPreview,
) -> AmazonPaymentImport:
    source_sha256 = calculate_sha256(content)

    existing = await db.scalar(
        select(AmazonPaymentImport).where(AmazonPaymentImport.source_sha256 == source_sha256)
    )
    if existing:
        raise DuplicateImportError(existing.id)

    period_start, period_end = _period_bounds(preview)
    payment_import = AmazonPaymentImport(
        source_filename=preview.filename,
        source_sha256=source_sha256,
        marketplace=marketplace,
        report_period_start=period_start,
        report_period_end=period_end,
        detected_locale=None,
        header_mapping=preview.mapping_result.mapping,
        row_count=preview.row_count,
    )
    db.add(payment_import)
    await db.flush()

    for row_number, raw_row in enumerate(preview.raw_rows, start=2):
        raw = AmazonPaymentTransactionRaw(
            import_id=payment_import.id,
            row_number=row_number,
            raw_row=raw_row,
        )
        db.add(raw)
        await db.flush()

        parsed = preview.parsed_rows[row_number - 2]
        transaction = AmazonPaymentTransaction(
            import_id=payment_import.id,
            raw_row_id=raw.id,
            marketplace=marketplace,
            currency=str(parsed["currency"]),
            transaction_date=parsed["transaction_date"],
            transaction_status=str(parsed["transaction_status"] or ""),
            transaction_type=str(parsed["transaction_type"] or ""),
            external_transaction_id=str(parsed["external_transaction_id"] or "") or None,
            sku=str(parsed["sku"] or "") or None,
            quantity=parsed["quantity"] if isinstance(parsed["quantity"], Decimal) else None,
            product_details=str(parsed["product_details"] or "") or None,
            product_charges=parsed["product_charges"] if isinstance(parsed["product_charges"], Decimal) else Decimal("0"),
            promotional_rebates=parsed["promotional_rebates"] if isinstance(parsed["promotional_rebates"], Decimal) else Decimal("0"),
            amazon_fees=parsed["amazon_fees"] if isinstance(parsed["amazon_fees"], Decimal) else Decimal("0"),
            other_amount=parsed["other_amount"] if isinstance(parsed["other_amount"], Decimal) else Decimal("0"),
            total_amount=parsed["total_amount"] if isinstance(parsed["total_amount"], Decimal) else Decimal("0"),
            raw_row=raw_row,
        )
        db.add(transaction)

    await db.commit()
    await db.refresh(payment_import)
    return payment_import
