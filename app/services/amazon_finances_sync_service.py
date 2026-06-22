import hashlib
import json
from dataclasses import dataclass
from datetime import date, datetime, time, timezone
from decimal import Decimal
from typing import Any

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.amazon_payment_import import AmazonPaymentImport
from app.models.amazon_payment_transaction import AmazonPaymentTransaction
from app.models.amazon_payment_transaction_raw import AmazonPaymentTransactionRaw
from app.services.amazon_sp_api_client import AmazonSpApiClient


@dataclass(frozen=True)
class AmazonFinancesSyncResult:
    status: str
    import_id: int | None
    marketplace: str
    transactions_received: int
    rows_imported: int
    rows_updated: int
    rows_skipped: int
    period_start: str
    period_end: str


class AmazonFinancesSyncConflict(RuntimeError):
    pass


def _amount(value: dict | None) -> Decimal:
    return Decimal(str((value or {}).get("currencyAmount") or 0))


def _direct_breakdown_amount(breakdowns: list[dict] | None, name: str) -> Decimal:
    return sum(
        (
            _amount(row.get("breakdownAmount"))
            for row in (breakdowns or [])
            if row.get("breakdownType") == name
        ),
        Decimal("0"),
    )


def _related_identifier(rows: list[dict] | None, name: str) -> str | None:
    for row in rows or []:
        if row.get("relatedIdentifierName") == name:
            return str(row.get("relatedIdentifierValue") or "") or None
    return None


def _product_context(item: dict) -> dict:
    return next(
        (
            row
            for row in item.get("contexts") or []
            if row.get("contextType") == "ProductContext"
        ),
        {},
    )


def _fulfillment_channel(value: str | None) -> str:
    normalized = (value or "").strip().upper()
    if normalized == "AFN":
        return "FBA"
    if normalized == "MFN":
        return "FBM"
    return normalized or "UNKNOWN"


def _context_quantity(context: dict, transaction_type: str) -> Decimal:
    for key in ("quantityShipped", "quantityReturned", "quantity"):
        if context.get(key) is not None:
            return Decimal(str(context.get(key) or 0))
    if context.get("sku") and "refund" in transaction_type.casefold():
        return Decimal("1")
    return Decimal("0")


def _transaction_type(transaction: dict) -> str:
    return str(
        transaction.get("description")
        or transaction.get("transactionType")
        or ""
    )


def _status_priority(value: str | None) -> int:
    return {
        "RELEASED": 30,
        "DEFERRED_RELEASED": 20,
        "DEFERRED": 10,
    }.get((value or "").strip().upper(), 0)


def _marketplace_code(marketplace: str) -> str:
    return marketplace.strip().upper()


def finance_transaction_rows(
    marketplace: str,
    transactions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    result_by_source_id: dict[str, dict[str, Any]] = {}
    for transaction in transactions:
        transaction_id = str(transaction.get("transactionId") or "")
        order_id = _related_identifier(
            transaction.get("relatedIdentifiers"),
            "ORDER_ID",
        )
        canonical_transaction_id = (
            _related_identifier(
                transaction.get("relatedIdentifiers"),
                "RELEASE_TRANSACTION_ID",
            )
            or transaction_id
        )
        items = transaction.get("items") or [None]
        for item_index, item in enumerate(items):
            values = item or transaction
            breakdowns = values.get("breakdowns") or []
            context = _product_context(item or {})
            product_charges = _direct_breakdown_amount(
                breakdowns,
                "ProductCharges",
            )
            promotional_rebates = _direct_breakdown_amount(
                breakdowns,
                "PromotionalRebates",
            )
            amazon_fees = _direct_breakdown_amount(
                breakdowns,
                "AmazonFees",
            )
            tax = _direct_breakdown_amount(breakdowns, "Tax")
            total_amount = _amount(values.get("totalAmount"))
            other_amount = (
                total_amount
                - product_charges
                - promotional_rebates
                - amazon_fees
                - tax
            )
            currency = str(
                (values.get("totalAmount") or {}).get("currencyCode")
                or (transaction.get("totalAmount") or {}).get("currencyCode")
                or "EUR"
            )
            posted_date = datetime.fromisoformat(
                str(transaction.get("postedDate")).replace("Z", "+00:00")
            ).date()
            source_event_id = (
                f"finances:{_marketplace_code(marketplace)}:{canonical_transaction_id}:{item_index}"
                if canonical_transaction_id
                else "finances:"
                + hashlib.sha256(
                    json.dumps(
                        {
                            "marketplace": marketplace,
                            "index": item_index,
                            "transaction": transaction,
                        },
                        sort_keys=True,
                    ).encode("utf-8")
                ).hexdigest()
            )
            normalized = {
                    "source_event_id": source_event_id,
                    "marketplace": _marketplace_code(marketplace),
                    "currency": currency,
                    "transaction_date": posted_date,
                    "transaction_status": str(
                        transaction.get("transactionStatus") or ""
                    ),
                    "transaction_type": _transaction_type(transaction),
                    "external_transaction_id": order_id,
                    "sku": str(context.get("sku") or "") or None,
                    "quantity": _context_quantity(
                        context,
                        _transaction_type(transaction),
                    ),
                    "fulfillment_channel": _fulfillment_channel(
                        context.get("fulfillmentNetwork")
                    ),
                    "product_details": str(
                        (item or {}).get("description")
                        or transaction.get("description")
                        or ""
                    )
                    or None,
                    "product_charges": product_charges,
                    "promotional_rebates": promotional_rebates,
                    "amazon_fees": amazon_fees,
                    "other_amount": other_amount,
                    "total_amount": total_amount,
                    "raw_row": {
                        "source": "sp_api_finances_v2024_06_19",
                        "transaction": transaction,
                        "item_index": item_index,
                        "tax_amount": str(tax),
                    },
                }
            previous = result_by_source_id.get(source_event_id)
            if previous is None or (
                _status_priority(normalized["transaction_status"]),
                normalized["transaction_date"],
            ) > (
                _status_priority(previous["transaction_status"]),
                previous["transaction_date"],
            ):
                result_by_source_id[source_event_id] = normalized
    return list(result_by_source_id.values())


def _utc_start(value: date) -> str:
    return datetime.combine(value, time.min, tzinfo=timezone.utc).isoformat().replace(
        "+00:00",
        "Z",
    )


def _utc_end(value: date) -> str:
    return datetime.combine(value, time.max, tzinfo=timezone.utc).isoformat().replace(
        "+00:00",
        "Z",
    )


async def sync_finance_transactions(
    db: AsyncSession,
    marketplace: str,
    start_date: date,
    end_date: date,
) -> AmazonFinancesSyncResult:
    marketplace = _marketplace_code(marketplace)
    overlapping_manual_import = await db.scalar(
        select(AmazonPaymentImport)
        .where(AmazonPaymentImport.marketplace == marketplace)
        .where(AmazonPaymentImport.detected_locale.is_distinct_from("api"))
        .where(AmazonPaymentImport.report_period_start.is_not(None))
        .where(AmazonPaymentImport.report_period_end.is_not(None))
        .where(AmazonPaymentImport.report_period_start <= datetime.combine(end_date, time.max))
        .where(AmazonPaymentImport.report_period_end >= datetime.combine(start_date, time.min))
        .limit(1)
    )
    if overlapping_manual_import:
        raise AmazonFinancesSyncConflict(
            "This period overlaps manual Payments import "
            f"{overlapping_manual_import.id} ({overlapping_manual_import.source_filename}). "
            "Delete the manual import before replacing that period with Finances API data."
        )
    sp_api = AmazonSpApiClient()
    async with httpx.AsyncClient(timeout=httpx.Timeout(120.0)) as client:
        transactions = await sp_api.list_finance_transactions(
            client=client,
            marketplace=marketplace,
            posted_after=_utc_start(start_date),
            posted_before=_utc_end(end_date),
        )
    rows = finance_transaction_rows(marketplace, transactions)
    source_ids = [row["source_event_id"] for row in rows]
    existing_rows = list(
        await db.scalars(
            select(AmazonPaymentTransaction).where(
                AmazonPaymentTransaction.source_event_id.in_(source_ids)
            )
        )
    ) if source_ids else []
    existing_by_id = {
        row.source_event_id: row
        for row in existing_rows
        if row.source_event_id
    }
    new_rows: list[dict[str, Any]] = []
    updated = 0
    skipped = 0
    for values in rows:
        existing = existing_by_id.get(values["source_event_id"])
        if existing is None:
            new_rows.append(values)
            continue
        if _status_priority(values["transaction_status"]) <= _status_priority(
            existing.transaction_status
        ):
            skipped += 1
            continue
        existing.marketplace = values["marketplace"]
        existing.currency = values["currency"]
        existing.transaction_date = values["transaction_date"]
        existing.transaction_status = values["transaction_status"]
        existing.transaction_type = values["transaction_type"]
        existing.external_transaction_id = values["external_transaction_id"]
        existing.sku = values["sku"]
        existing.quantity = values["quantity"]
        existing.fulfillment_channel = values["fulfillment_channel"]
        existing.product_details = values["product_details"]
        existing.product_charges = values["product_charges"]
        existing.promotional_rebates = values["promotional_rebates"]
        existing.amazon_fees = values["amazon_fees"]
        existing.other_amount = values["other_amount"]
        existing.total_amount = values["total_amount"]
        existing.raw_row = values["raw_row"]
        raw = await db.get(AmazonPaymentTransactionRaw, existing.raw_row_id)
        if raw:
            raw.raw_row = values["raw_row"]
        updated += 1
    if not new_rows:
        await db.commit()
        return AmazonFinancesSyncResult(
            status="updated" if updated else "no_new_rows",
            import_id=None,
            marketplace=marketplace,
            transactions_received=len(transactions),
            rows_imported=0,
            rows_updated=updated,
            rows_skipped=skipped,
            period_start=start_date.isoformat(),
            period_end=end_date.isoformat(),
        )

    payment_import = AmazonPaymentImport(
        source_filename=(
            f"sp-api-finances-{marketplace}-{start_date.isoformat()}-"
            f"{end_date.isoformat()}.json"
        ),
        source_sha256=None,
        marketplace=marketplace,
        report_period_start=datetime.combine(start_date, time.min),
        report_period_end=datetime.combine(end_date, time.min),
        detected_locale="api",
        header_mapping={"source": "sp_api_finances_v2024_06_19"},
        row_count=len(new_rows),
    )
    db.add(payment_import)
    await db.flush()
    for row_number, values in enumerate(new_rows, start=1):
        raw = AmazonPaymentTransactionRaw(
            import_id=payment_import.id,
            row_number=row_number,
            raw_row=values["raw_row"],
        )
        db.add(raw)
        await db.flush()
        db.add(
            AmazonPaymentTransaction(
                import_id=payment_import.id,
                raw_row_id=raw.id,
                source_event_id=values["source_event_id"],
                marketplace=values["marketplace"],
                currency=values["currency"],
                transaction_date=values["transaction_date"],
                transaction_status=values["transaction_status"],
                transaction_type=values["transaction_type"],
                external_transaction_id=values["external_transaction_id"],
                sku=values["sku"],
                quantity=values["quantity"],
                fulfillment_channel=values["fulfillment_channel"],
                product_details=values["product_details"],
                product_charges=values["product_charges"],
                promotional_rebates=values["promotional_rebates"],
                amazon_fees=values["amazon_fees"],
                other_amount=values["other_amount"],
                total_amount=values["total_amount"],
                raw_row=values["raw_row"],
            )
        )
    await db.commit()
    await db.refresh(payment_import)
    return AmazonFinancesSyncResult(
        status="imported",
        import_id=payment_import.id,
        marketplace=marketplace,
        transactions_received=len(transactions),
        rows_imported=len(new_rows),
        rows_updated=updated,
        rows_skipped=skipped,
        period_start=start_date.isoformat(),
        period_end=end_date.isoformat(),
    )
