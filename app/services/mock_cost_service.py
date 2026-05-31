import hashlib
from datetime import date
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.amazon_payment_transaction import AmazonPaymentTransaction
from app.models.product_cost import ProductCost
from app.models.product_cost_import import ProductCostImport
from app.services.fx import convert_to_eur_with_rate, get_latest_fx_rates, get_rate_for_currency
from app.services.transaction_classifier import is_order_payment


def make_mock_sku(product_details: str) -> str:
    digest = hashlib.sha1(product_details.encode("utf-8")).hexdigest()[:10].upper()
    return f"MOCK-{digest}"


async def create_mock_costs_from_transactions(
    db: AsyncSession,
    effective_date: date,
    cost_ratio: Decimal,
) -> ProductCostImport:
    fingerprint = hashlib.sha256(
        f"mock_from_transactions:{effective_date.isoformat()}:{cost_ratio}".encode("utf-8")
    ).hexdigest()
    existing_import = await db.scalar(
        select(ProductCostImport).where(ProductCostImport.source_sha256 == fingerprint)
    )
    if existing_import:
        return existing_import

    rates = await get_latest_fx_rates(db)
    existing_names = set(
        await db.scalars(
            select(ProductCost.product_name).where(ProductCost.product_name.is_not(None))
        )
    )

    result = await db.execute(
        select(
            AmazonPaymentTransaction.product_details,
            AmazonPaymentTransaction.currency,
            func.avg(AmazonPaymentTransaction.product_charges).label("avg_product_charges"),
            func.count().label("rows"),
        )
        .where(AmazonPaymentTransaction.product_details.is_not(None))
        .where(AmazonPaymentTransaction.product_details != "")
        .group_by(AmazonPaymentTransaction.product_details, AmazonPaymentTransaction.currency)
    )

    candidates = []
    for row in result:
        if row.product_details in existing_names:
            continue
        sample_type = await db.scalar(
            select(AmazonPaymentTransaction.transaction_type)
            .where(AmazonPaymentTransaction.product_details == row.product_details)
            .limit(1)
        )
        if not is_order_payment(sample_type):
            continue
        rate_to_eur = get_rate_for_currency(rates, row.currency)
        avg_charge_eur = convert_to_eur_with_rate(row.avg_product_charges, rate_to_eur)
        mock_cost = (avg_charge_eur * cost_ratio).quantize(Decimal("0.01"))
        if mock_cost <= 0:
            continue
        candidates.append(
            {
                "sku": make_mock_sku(row.product_details),
                "product_name": row.product_details,
                "purchase_cost": mock_cost,
                "currency": "EUR",
                "effective_date": effective_date,
                "raw_row": {
                    "source": "mock_from_transactions",
                    "product_details": row.product_details,
                    "transaction_currency": row.currency,
                    "avg_product_charges": str(row.avg_product_charges),
                    "cost_ratio": str(cost_ratio),
                    "rows": row.rows,
                },
            }
        )

    cost_import = ProductCostImport(
        source_filename=f"mock_from_transactions_{effective_date.isoformat()}",
        source_sha256=fingerprint,
        currency="EUR",
        effective_date=effective_date,
        header_mapping={
            "product_name": "product_details",
            "sku": "generated_mock_sku",
            "purchase_cost": "avg_product_charges_eur * cost_ratio",
        },
        row_count=len(candidates),
    )
    db.add(cost_import)
    await db.flush()

    for candidate in candidates:
        db.add(ProductCost(import_id=cost_import.id, **candidate))

    await db.commit()
    await db.refresh(cost_import)
    return cost_import
