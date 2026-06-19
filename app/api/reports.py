from datetime import date
from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy import Select, case, func, literal, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.models.amazon_order_item import AmazonOrderItem
from app.models.amazon_payment_transaction import AmazonPaymentTransaction
from app.models.product_cost import ProductCost
from app.models.product_mapping import ProductMapping
from app.models.purchase_invoice import PurchaseInvoice
from app.models.purchase_invoice_line import PurchaseInvoiceLine
from app.services.fx import (
    convert_to_eur_with_rate,
    get_fx_rate_history,
    get_latest_fx_rates,
    get_rate_for_currency,
    get_rate_on_date,
)
from app.services.app_settings import get_fulfillment_cost_settings
from app.services.fifo_cost_service import fifo_event_costs
from app.services.product_mapping_service import product_similarity
from app.services.transaction_classifier import classify_payment_type, is_order_payment


router = APIRouter(prefix="/reports", tags=["reports"])


class PaymentSummaryRow(BaseModel):
    month: str
    marketplace: str
    currency: str
    fx_rate_to_eur: float
    transaction_type: str
    rows: int
    product_charges: float
    promotional_rebates: float
    amazon_fees: float
    other_amount: float
    total_amount: float
    product_charges_eur: float
    promotional_rebates_eur: float
    amazon_fees_eur: float
    other_amount_eur: float
    total_amount_eur: float


class CurrencyTotalRow(BaseModel):
    currency: str
    rows: int
    product_charges: float
    promotional_rebates: float
    amazon_fees: float
    other_amount: float
    total_amount: float


class GeneralTotalRow(BaseModel):
    rows: int
    product_charges_eur: float
    promotional_rebates_eur: float
    amazon_fees_eur: float
    other_amount_eur: float
    total_amount_eur: float


class MonthlyCashflowResponse(BaseModel):
    start_date: str | None
    end_date: str | None
    rows: list[PaymentSummaryRow]
    totals_by_currency: list[CurrencyTotalRow]
    general_total_eur: GeneralTotalRow


class ProductCostRow(BaseModel):
    id: int
    sku: str
    ean: str | None
    product_name: str | None
    purchase_cost: float
    currency: str
    effective_date: str


class ProductCostLatestResponse(BaseModel):
    rows: list[ProductCostRow]


class AmazonPnlCategoryRow(BaseModel):
    category: str
    transaction_type: str
    fulfillment_channel: str
    rows: int
    units: float
    product_charges_eur: float
    promotional_rebates_eur: float
    amazon_fees_eur: float
    other_amount_eur: float
    total_amount_eur: float


class AmazonPnlSummary(BaseModel):
    rows: int
    order_rows: int
    refund_rows: int
    units_sold: float
    units_refunded: float
    gross_sales_eur: float
    promotional_rebates_eur: float
    refunds_eur: float
    amazon_fees_eur: float
    service_other_fees_eur: float
    transfers_eur: float
    amazon_operating_result_eur: float
    ledger_total_eur: float


class AmazonPnlResponse(BaseModel):
    start_date: str | None
    end_date: str | None
    summary: AmazonPnlSummary
    rows: list[AmazonPnlCategoryRow]


class MissingCostRow(BaseModel):
    sku: str | None
    product_details: str
    units_estimated: int
    revenue_eur: float
    average_selling_price_eur: float | None


class UnknownTransactionTypeRow(BaseModel):
    transaction_type: str
    rows: int
    total_amount_eur: float


class ReconciliationRow(BaseModel):
    category: str
    status: str
    external_transaction_id: str | None
    sku: str | None
    transaction_type: str
    payment_rows: int
    payment_units: float
    order_units: float | None
    amount_eur: float


class DataQualitySummary(BaseModel):
    payment_rows: int
    rows_with_sku: int
    rows_without_sku: int
    sold_skus: int
    missing_cost_skus: int
    unknown_transaction_types: int
    order_groups: int
    matched_order_groups: int
    unmatched_order_groups: int
    quantity_mismatch_groups: int
    order_match_percent: float | None
    matched_order_units: float
    unmatched_order_units: float
    refund_groups: int
    return_fee_groups: int


class DataQualityResponse(BaseModel):
    start_date: str | None
    end_date: str | None
    summary: DataQualitySummary
    missing_costs: list[MissingCostRow]
    unknown_transaction_types: list[UnknownTransactionTypeRow]
    reconciliation_rows: list[ReconciliationRow]


class ProductProfitabilityRow(BaseModel):
    product_details: str
    asin: str | None
    sku: str | None
    ean: str | None
    fulfillment_channel: str
    currency: str
    fx_rate_to_eur: float
    transaction_rows: int
    units_estimated: int
    units_refunded: int
    revenue_original: float
    revenue_gross_eur: float
    sales_vat_eur: float
    revenue_eur: float
    refunds_eur: float
    promotional_rebates_eur: float
    amazon_fees_eur: float
    other_amount_eur: float
    prep_cost_eur: float
    storage_cost_eur: float
    fbm_logistics_cost_eur: float
    operational_cost_eur: float
    average_selling_price_eur: float | None
    purchase_cost_eur: float | None
    cogs_eur: float | None
    gross_profit_eur: float | None
    net_profit_eur: float | None
    margin_percent: float | None
    roi_percent: float | None
    net_margin_percent: float | None
    net_roi_percent: float | None
    profitability_status: str
    cost_match_status: str


def raw_lookup(raw_row: dict | None, *keys: str) -> str | None:
    if not raw_row:
        return None
    normalized = {str(key).lower(): value for key, value in raw_row.items()}
    for key in keys:
        value = raw_row.get(key) or normalized.get(key.lower())
        if value:
            return str(value)
    return None


def best_product_name_match(
    product_details: str,
    candidates: list[tuple[str, object]],
    min_score: Decimal = Decimal("60"),
) -> object | None:
    best_item = None
    best_score = Decimal("0")
    for name, item in candidates:
        score = product_similarity(product_details, name)
        if score > best_score:
            best_item = item
            best_score = score
    return best_item if best_score >= min_score else None


def best_product_alias_match(
    product_details_aliases: set[str],
    candidates: list[tuple[str, object]],
    min_score: Decimal = Decimal("60"),
) -> object | None:
    best_item = None
    best_score = Decimal("0")
    for product_details in product_details_aliases:
        for name, item in candidates:
            score = product_similarity(product_details, name)
            if score > best_score:
                best_item = item
                best_score = score
    return best_item if best_score >= min_score else None


class ProductProfitabilitySummary(BaseModel):
    products: int
    matched_products: int
    missing_cost_products: int
    units_estimated: int
    units_refunded: int
    revenue_gross_eur: float
    sales_vat_eur: float
    revenue_eur: float
    refunds_eur: float
    promotional_rebates_eur: float
    amazon_fees_eur: float
    other_amount_eur: float
    operational_cost_eur: float
    cogs_eur: float
    gross_profit_eur: float
    net_profit_eur: float
    margin_percent: float | None
    roi_percent: float | None
    net_margin_percent: float | None
    net_roi_percent: float | None
    profitable_products: int
    loss_products: int
    breakeven_products: int


def profitability_status(gross_profit_eur: float | None) -> str:
    if gross_profit_eur is None:
        return "unknown"
    if gross_profit_eur > 0:
        return "profitable"
    if gross_profit_eur < 0:
        return "loss"
    return "breakeven"


class ProductProfitabilityResponse(BaseModel):
    summary: ProductProfitabilitySummary
    rows: list[ProductProfitabilityRow]


class PurchaseSummaryRow(BaseModel):
    month: str
    supplier_name: str
    currency: str
    invoices: int
    lines: int
    product_lines: int
    expense_lines: int
    quantity: float
    subtotal_amount: float
    product_subtotal_amount: float
    expense_subtotal_amount: float
    inbound_shipping_amount: float
    fulfillment_fee_amount: float
    marketplace_fee_amount: float
    other_service_amount: float
    vat_amount: float
    total_amount: float


class PurchaseSummaryResponse(BaseModel):
    rows: list[PurchaseSummaryRow]


def money(value: Decimal | int | float | None) -> float:
    return float(value or 0)


def eur(value: Decimal | int | float | None, rate_to_eur: Decimal) -> float:
    return money(convert_to_eur_with_rate(value, rate_to_eur))


def apply_date_filters(query: Select, start_date: date | None, end_date: date | None) -> Select:
    if start_date:
        query = query.where(AmazonPaymentTransaction.transaction_date >= start_date)
    if end_date:
        query = query.where(AmazonPaymentTransaction.transaction_date <= end_date)
    return query


def apply_invoice_date_filters(query: Select, start_date: date | None, end_date: date | None) -> Select:
    if start_date:
        query = query.where(PurchaseInvoice.invoice_date >= start_date)
    if end_date:
        query = query.where(PurchaseInvoice.invoice_date <= end_date)
    return query


@router.get("/monthly-cashflow", response_model=MonthlyCashflowResponse)
async def monthly_cashflow(
    db: Annotated[AsyncSession, Depends(get_db)],
    start_date: Annotated[date | None, Query()] = None,
    end_date: Annotated[date | None, Query()] = None,
) -> MonthlyCashflowResponse:
    query = select(
        AmazonPaymentTransaction.transaction_date,
        AmazonPaymentTransaction.marketplace,
        AmazonPaymentTransaction.currency,
        AmazonPaymentTransaction.transaction_type,
        func.count().label("rows"),
        func.coalesce(func.sum(AmazonPaymentTransaction.product_charges), 0).label("product_charges"),
        func.coalesce(func.sum(AmazonPaymentTransaction.promotional_rebates), 0).label("promotional_rebates"),
        func.coalesce(func.sum(AmazonPaymentTransaction.amazon_fees), 0).label("amazon_fees"),
        func.coalesce(func.sum(AmazonPaymentTransaction.other_amount), 0).label("other_amount"),
        func.coalesce(func.sum(AmazonPaymentTransaction.total_amount), 0).label("total_amount"),
    )
    query = apply_date_filters(query, start_date, end_date)
    query = query.group_by(
        AmazonPaymentTransaction.transaction_date,
        AmazonPaymentTransaction.marketplace,
        AmazonPaymentTransaction.currency,
        AmazonPaymentTransaction.transaction_type,
    ).order_by(
        AmazonPaymentTransaction.transaction_date,
        AmazonPaymentTransaction.marketplace,
        AmazonPaymentTransaction.transaction_type,
    )

    result = await db.execute(query)
    history = await get_fx_rate_history(db)
    buckets: dict[tuple[str, str, str, str], dict[str, float | int]] = {}
    for row in result:
        rate_to_eur = get_rate_on_date(history, row.currency, row.transaction_date)
        key = (
            row.transaction_date.replace(day=1).isoformat(),
            row.marketplace,
            row.currency,
            row.transaction_type,
        )
        bucket = buckets.setdefault(
            key,
            {
                "rows": 0,
                "product_charges": 0.0,
                "promotional_rebates": 0.0,
                "amazon_fees": 0.0,
                "other_amount": 0.0,
                "total_amount": 0.0,
                "product_charges_eur": 0.0,
                "promotional_rebates_eur": 0.0,
                "amazon_fees_eur": 0.0,
                "other_amount_eur": 0.0,
                "total_amount_eur": 0.0,
                "fx_weighted": 0.0,
                "fx_weight": 0.0,
            },
        )
        bucket["rows"] = int(bucket["rows"]) + int(row.rows)
        for field in ("product_charges", "promotional_rebates", "amazon_fees", "other_amount", "total_amount"):
            bucket[field] = round(float(bucket[field]) + money(getattr(row, field)), 2)
            bucket[f"{field}_eur"] = round(
                float(bucket[f"{field}_eur"]) + eur(getattr(row, field), rate_to_eur),
                2,
            )
        weight = abs(money(row.total_amount)) or abs(money(row.product_charges)) or 1
        bucket["fx_weighted"] = float(bucket["fx_weighted"]) + money(rate_to_eur) * weight
        bucket["fx_weight"] = float(bucket["fx_weight"]) + weight

    rows = []
    for (month, marketplace, currency, transaction_type), bucket in buckets.items():
        fx_weight = float(bucket.pop("fx_weight"))
        fx_weighted = float(bucket.pop("fx_weighted"))
        rows.append(
            PaymentSummaryRow(
                month=month,
                marketplace=marketplace,
                currency=currency,
                fx_rate_to_eur=round(fx_weighted / fx_weight, 8) if fx_weight else 1,
                transaction_type=transaction_type,
                **bucket,
            )
        )

    totals: dict[str, dict[str, int | float]] = {}
    general_total = {
        "rows": 0,
        "product_charges_eur": 0.0,
        "promotional_rebates_eur": 0.0,
        "amazon_fees_eur": 0.0,
        "other_amount_eur": 0.0,
        "total_amount_eur": 0.0,
    }
    for row in rows:
        bucket = totals.setdefault(
            row.currency,
            {
                "rows": 0,
                "product_charges": 0.0,
                "promotional_rebates": 0.0,
                "amazon_fees": 0.0,
                "other_amount": 0.0,
                "total_amount": 0.0,
            },
        )
        bucket["rows"] = int(bucket["rows"]) + row.rows
        for field in (
            "product_charges",
            "promotional_rebates",
            "amazon_fees",
            "other_amount",
            "total_amount",
        ):
            bucket[field] = round(float(bucket[field]) + getattr(row, field), 2)
        general_total["rows"] = int(general_total["rows"]) + row.rows
        for field in (
            "product_charges_eur",
            "promotional_rebates_eur",
            "amazon_fees_eur",
            "other_amount_eur",
            "total_amount_eur",
        ):
            general_total[field] = round(float(general_total[field]) + getattr(row, field), 2)

    return MonthlyCashflowResponse(
        start_date=start_date.isoformat() if start_date else None,
        end_date=end_date.isoformat() if end_date else None,
        rows=rows,
        totals_by_currency=[
            CurrencyTotalRow(currency=currency, **values)
            for currency, values in sorted(totals.items())
        ],
        general_total_eur=GeneralTotalRow(**general_total),
    )


@router.get("/product-costs/latest", response_model=ProductCostLatestResponse)
async def latest_product_costs(
    db: Annotated[AsyncSession, Depends(get_db)],
    limit: Annotated[int, Query(ge=1, le=500)] = 100,
) -> ProductCostLatestResponse:
    result = await db.scalars(
        select(ProductCost).order_by(
            ProductCost.sku,
            ProductCost.effective_date.desc(),
            ProductCost.id.desc(),
        )
    )
    latest_by_sku: dict[str, ProductCost] = {}
    for row in result:
        latest_by_sku.setdefault(row.sku, row)

    return ProductCostLatestResponse(
        rows=[
            ProductCostRow(
                id=row.id,
                sku=row.sku,
                ean=raw_lookup(row.raw_row, "ean", "EAN") or raw_lookup(row.raw_row.get("raw_row"), "ean", "EAN"),
                product_name=row.product_name,
                purchase_cost=money(row.purchase_cost),
                currency=row.currency,
                effective_date=row.effective_date.isoformat(),
            )
            for row in list(latest_by_sku.values())[:limit]
        ]
    )


@router.get("/amazon-pnl", response_model=AmazonPnlResponse)
async def amazon_pnl(
    db: Annotated[AsyncSession, Depends(get_db)],
    start_date: Annotated[date | None, Query()] = None,
    end_date: Annotated[date | None, Query()] = None,
) -> AmazonPnlResponse:
    query = select(
        AmazonPaymentTransaction.transaction_date,
        AmazonPaymentTransaction.transaction_type,
        AmazonPaymentTransaction.fulfillment_channel,
        AmazonPaymentTransaction.currency,
        func.count().label("rows"),
        func.coalesce(func.sum(AmazonPaymentTransaction.quantity), 0).label("quantity"),
        func.coalesce(func.sum(AmazonPaymentTransaction.product_charges), 0).label("product_charges"),
        func.coalesce(func.sum(AmazonPaymentTransaction.promotional_rebates), 0).label("promotional_rebates"),
        func.coalesce(func.sum(AmazonPaymentTransaction.amazon_fees), 0).label("amazon_fees"),
        func.coalesce(func.sum(AmazonPaymentTransaction.other_amount), 0).label("other_amount"),
        func.coalesce(func.sum(AmazonPaymentTransaction.total_amount), 0).label("total_amount"),
    )
    query = apply_date_filters(query, start_date, end_date)
    query = query.group_by(
        AmazonPaymentTransaction.transaction_date,
        AmazonPaymentTransaction.transaction_type,
        AmazonPaymentTransaction.fulfillment_channel,
        AmazonPaymentTransaction.currency,
    ).order_by(
        AmazonPaymentTransaction.transaction_type,
        AmazonPaymentTransaction.fulfillment_channel,
        AmazonPaymentTransaction.currency,
    )
    result = await db.execute(query)
    history = await get_fx_rate_history(db)

    category_buckets: dict[tuple[str, str, str], dict[str, float | int]] = {}
    summary = {
        "rows": 0,
        "order_rows": 0,
        "refund_rows": 0,
        "units_sold": 0.0,
        "units_refunded": 0.0,
        "gross_sales_eur": 0.0,
        "promotional_rebates_eur": 0.0,
        "refunds_eur": 0.0,
        "amazon_fees_eur": 0.0,
        "service_other_fees_eur": 0.0,
        "transfers_eur": 0.0,
        "ledger_total_eur": 0.0,
    }
    for row in result:
        category = classify_payment_type(row.transaction_type)
        rate_to_eur = get_rate_on_date(
            history,
            row.currency,
            row.transaction_date,
        )
        product_charges_eur = eur(row.product_charges, rate_to_eur)
        promotional_rebates_eur = eur(row.promotional_rebates, rate_to_eur)
        amazon_fees_eur = eur(row.amazon_fees, rate_to_eur)
        other_amount_eur = eur(row.other_amount, rate_to_eur)
        total_amount_eur = eur(row.total_amount, rate_to_eur)
        quantity = money(row.quantity)
        key = (category, row.transaction_type, row.fulfillment_channel)
        bucket = category_buckets.setdefault(
            key,
            {
                "rows": 0,
                "units": 0.0,
                "product_charges_eur": 0.0,
                "promotional_rebates_eur": 0.0,
                "amazon_fees_eur": 0.0,
                "other_amount_eur": 0.0,
                "total_amount_eur": 0.0,
            },
        )
        bucket["rows"] = int(bucket["rows"]) + int(row.rows)
        bucket["units"] = round(float(bucket["units"]) + quantity, 3)
        for field, value in (
            ("product_charges_eur", product_charges_eur),
            ("promotional_rebates_eur", promotional_rebates_eur),
            ("amazon_fees_eur", amazon_fees_eur),
            ("other_amount_eur", other_amount_eur),
            ("total_amount_eur", total_amount_eur),
        ):
            bucket[field] = round(float(bucket[field]) + value, 2)
        summary["rows"] += int(row.rows)
        summary["amazon_fees_eur"] = round(summary["amazon_fees_eur"] + amazon_fees_eur, 2)
        summary["ledger_total_eur"] = round(summary["ledger_total_eur"] + total_amount_eur, 2)
        if category == "order":
            summary["order_rows"] += int(row.rows)
            summary["units_sold"] = round(summary["units_sold"] + quantity, 3)
            summary["gross_sales_eur"] = round(summary["gross_sales_eur"] + product_charges_eur, 2)
            summary["promotional_rebates_eur"] = round(summary["promotional_rebates_eur"] + promotional_rebates_eur, 2)
        elif category == "refund":
            summary["refund_rows"] += int(row.rows)
            summary["units_refunded"] = round(summary["units_refunded"] + quantity, 3)
            summary["refunds_eur"] = round(summary["refunds_eur"] + product_charges_eur + promotional_rebates_eur, 2)
        elif category == "transfer":
            summary["transfers_eur"] = round(summary["transfers_eur"] + total_amount_eur, 2)
        elif category in {"service_fee", "fba_fee", "return_fee", "other"}:
            summary["service_other_fees_eur"] = round(
                summary["service_other_fees_eur"] + other_amount_eur,
                2,
            )

    rows = [
        AmazonPnlCategoryRow(
            category=category,
            transaction_type=transaction_type,
            fulfillment_channel=fulfillment_channel,
            **values,
        )
        for (category, transaction_type, fulfillment_channel), values in sorted(
            category_buckets.items()
        )
    ]
    amazon_operating_result_eur = round(
        summary["gross_sales_eur"]
        + summary["promotional_rebates_eur"]
        + summary["refunds_eur"]
        + summary["amazon_fees_eur"]
        + summary["service_other_fees_eur"],
        2,
    )
    return AmazonPnlResponse(
        start_date=start_date.isoformat() if start_date else None,
        end_date=end_date.isoformat() if end_date else None,
        summary=AmazonPnlSummary(
            **summary,
            amazon_operating_result_eur=amazon_operating_result_eur,
        ),
        rows=rows,
    )


@router.get("/data-quality", response_model=DataQualityResponse)
async def data_quality(
    db: Annotated[AsyncSession, Depends(get_db)],
    start_date: Annotated[date | None, Query()] = None,
    end_date: Annotated[date | None, Query()] = None,
    limit: Annotated[int, Query(ge=1, le=500)] = 100,
) -> DataQualityResponse:
    rates = await get_latest_fx_rates(db)

    row_query = select(
        func.count().label("payment_rows"),
        func.coalesce(
            func.sum(case(((AmazonPaymentTransaction.sku.is_not(None)) & (AmazonPaymentTransaction.sku != ""), 1), else_=0)),
            0,
        ).label("rows_with_sku"),
    )
    row_query = apply_date_filters(row_query, start_date, end_date)
    row_counts = (await db.execute(row_query)).one()

    cost_skus = {
        sku
        for sku in await db.scalars(select(ProductCost.sku).where(ProductCost.sku.is_not(None)).where(ProductCost.sku != ""))
    }

    sold_query = select(
        AmazonPaymentTransaction.sku,
        AmazonPaymentTransaction.product_details,
        AmazonPaymentTransaction.currency,
        AmazonPaymentTransaction.transaction_type,
        func.count().label("rows"),
        func.coalesce(func.sum(AmazonPaymentTransaction.quantity), 0).label("quantity"),
        func.coalesce(func.sum(AmazonPaymentTransaction.product_charges), 0).label("revenue_original"),
    )
    sold_query = apply_date_filters(sold_query, start_date, end_date)
    sold_query = (
        sold_query.where(AmazonPaymentTransaction.product_details.is_not(None))
        .where(AmazonPaymentTransaction.product_details != "")
        .group_by(
            AmazonPaymentTransaction.sku,
            AmazonPaymentTransaction.product_details,
            AmazonPaymentTransaction.currency,
            AmazonPaymentTransaction.transaction_type,
        )
    )
    sold_rows = await db.execute(sold_query)
    sold_products: dict[tuple[str, str], dict[str, str | int | float | None]] = {}
    for row in sold_rows:
        if not is_order_payment(row.transaction_type):
            continue
        key = (row.sku or row.product_details or "", row.currency)
        bucket = sold_products.setdefault(
            key,
            {
                "sku": row.sku,
                "product_details": row.product_details,
                "units_estimated": 0,
                "revenue_eur": 0.0,
            },
        )
        quantity = money(row.quantity)
        bucket["units_estimated"] = int(bucket["units_estimated"] or 0) + int(quantity if quantity else row.rows)
        rate_to_eur = get_rate_for_currency(rates, row.currency)
        bucket["revenue_eur"] = round(float(bucket["revenue_eur"] or 0) + eur(row.revenue_original, rate_to_eur), 2)

    missing_costs = [
        MissingCostRow(
            sku=str(bucket["sku"]) if bucket["sku"] else None,
            product_details=str(bucket["product_details"] or ""),
            units_estimated=int(bucket["units_estimated"] or 0),
            revenue_eur=float(bucket["revenue_eur"] or 0),
            average_selling_price_eur=(
                round(float(bucket["revenue_eur"] or 0) / int(bucket["units_estimated"] or 0), 2)
                if int(bucket["units_estimated"] or 0)
                else None
            ),
        )
        for bucket in sold_products.values()
        if not bucket["sku"] or str(bucket["sku"]) not in cost_skus
    ]
    missing_costs.sort(key=lambda row: row.revenue_eur, reverse=True)

    type_query = select(
        AmazonPaymentTransaction.transaction_type,
        AmazonPaymentTransaction.currency,
        func.count().label("rows"),
        func.coalesce(func.sum(AmazonPaymentTransaction.total_amount), 0).label("total_amount"),
    )
    type_query = apply_date_filters(type_query, start_date, end_date)
    type_query = type_query.group_by(AmazonPaymentTransaction.transaction_type, AmazonPaymentTransaction.currency)
    type_rows = await db.execute(type_query)
    unknown_types: list[UnknownTransactionTypeRow] = []
    for row in type_rows:
        if classify_payment_type(row.transaction_type) not in {"unknown", "other"}:
            continue
        rate_to_eur = get_rate_for_currency(rates, row.currency)
        unknown_types.append(
            UnknownTransactionTypeRow(
                transaction_type=row.transaction_type,
                rows=int(row.rows),
                total_amount_eur=eur(row.total_amount, rate_to_eur),
            )
        )
    unknown_types.sort(key=lambda row: abs(row.total_amount_eur), reverse=True)

    reconciliation_query = select(
        AmazonPaymentTransaction.external_transaction_id,
        AmazonPaymentTransaction.sku,
        AmazonPaymentTransaction.currency,
        AmazonPaymentTransaction.transaction_type,
        func.count().label("rows"),
        func.coalesce(func.sum(AmazonPaymentTransaction.quantity), 0).label("quantity"),
        func.coalesce(func.sum(AmazonPaymentTransaction.total_amount), 0).label("total_amount"),
    )
    reconciliation_query = apply_date_filters(reconciliation_query, start_date, end_date)
    reconciliation_query = (
        reconciliation_query.where(AmazonPaymentTransaction.external_transaction_id.is_not(None))
        .where(AmazonPaymentTransaction.external_transaction_id != "")
        .group_by(
            AmazonPaymentTransaction.external_transaction_id,
            AmazonPaymentTransaction.sku,
            AmazonPaymentTransaction.currency,
            AmazonPaymentTransaction.transaction_type,
        )
    )
    reconciliation_payment_rows = await db.execute(reconciliation_query)

    order_items = await db.scalars(select(AmazonOrderItem))
    order_units_by_key: dict[tuple[str, str], float] = {}
    for item in order_items:
        key = (item.amazon_order_id, item.sku)
        order_units_by_key[key] = round(
            order_units_by_key.get(key, 0.0) + money(item.quantity),
            3,
        )

    reconciliation_rows: list[ReconciliationRow] = []
    order_groups = 0
    matched_order_groups = 0
    unmatched_order_groups = 0
    quantity_mismatch_groups = 0
    matched_order_units = 0.0
    unmatched_order_units = 0.0
    refund_groups = 0
    return_fee_groups = 0

    for row in reconciliation_payment_rows:
        category = classify_payment_type(row.transaction_type)
        if category not in {"order", "refund", "return_fee"}:
            continue

        payment_units = money(row.quantity)
        order_key = (
            str(row.external_transaction_id or ""),
            str(row.sku or ""),
        )
        order_units = order_units_by_key.get(order_key)
        if category == "order":
            order_groups += 1
            if order_units is None:
                unmatched_order_groups += 1
                unmatched_order_units = round(unmatched_order_units + payment_units, 3)
                status = "unmatched"
            elif abs(order_units - payment_units) <= 0.001:
                matched_order_groups += 1
                matched_order_units = round(matched_order_units + payment_units, 3)
                status = "matched"
            else:
                quantity_mismatch_groups += 1
                unmatched_order_units = round(unmatched_order_units + payment_units, 3)
                status = "quantity_mismatch"
        elif category == "refund":
            refund_groups += 1
            status = "refund_pending"
        else:
            return_fee_groups += 1
            status = "return_fee_pending"

        rate_to_eur = get_rate_for_currency(rates, row.currency)
        reconciliation_rows.append(
            ReconciliationRow(
                category=category,
                status=status,
                external_transaction_id=row.external_transaction_id,
                sku=row.sku,
                transaction_type=row.transaction_type,
                payment_rows=int(row.rows),
                payment_units=payment_units,
                order_units=order_units,
                amount_eur=eur(row.total_amount, rate_to_eur),
            )
        )

    reconciliation_rows.sort(
        key=lambda row: (
            row.status == "matched",
            -abs(row.amount_eur),
            row.external_transaction_id or "",
            row.sku or "",
        )
    )

    return DataQualityResponse(
        start_date=start_date.isoformat() if start_date else None,
        end_date=end_date.isoformat() if end_date else None,
        summary=DataQualitySummary(
            payment_rows=int(row_counts.payment_rows or 0),
            rows_with_sku=int(row_counts.rows_with_sku or 0),
            rows_without_sku=int(row_counts.payment_rows or 0) - int(row_counts.rows_with_sku or 0),
            sold_skus=len(sold_products),
            missing_cost_skus=len(missing_costs),
            unknown_transaction_types=len(unknown_types),
            order_groups=order_groups,
            matched_order_groups=matched_order_groups,
            unmatched_order_groups=unmatched_order_groups,
            quantity_mismatch_groups=quantity_mismatch_groups,
            order_match_percent=(
                round(matched_order_groups / order_groups * 100, 1)
                if order_groups
                else None
            ),
            matched_order_units=matched_order_units,
            unmatched_order_units=unmatched_order_units,
            refund_groups=refund_groups,
            return_fee_groups=return_fee_groups,
        ),
        missing_costs=missing_costs[:limit],
        unknown_transaction_types=unknown_types[:limit],
        reconciliation_rows=[
            row
            for row in reconciliation_rows
            if row.status != "matched"
        ][:limit],
    )


@router.get("/product-profitability", response_model=ProductProfitabilityResponse)
async def product_profitability(
    db: Annotated[AsyncSession, Depends(get_db)],
    limit: Annotated[int, Query(ge=1, le=10000)] = 5000,
    start_date: Annotated[date | None, Query()] = None,
    end_date: Annotated[date | None, Query()] = None,
) -> ProductProfitabilityResponse:
    rates = await get_latest_fx_rates(db)
    fx_history = await get_fx_rate_history(db)
    fulfillment_costs = await get_fulfillment_cost_settings(db)
    fifo_costs = await fifo_event_costs(db, end_date)

    transaction_query = (
        select(
            AmazonPaymentTransaction.product_details,
            AmazonPaymentTransaction.sku,
            AmazonPaymentTransaction.external_transaction_id,
            AmazonPaymentTransaction.transaction_date,
            AmazonPaymentTransaction.marketplace,
            AmazonPaymentTransaction.fulfillment_channel,
            AmazonPaymentTransaction.currency,
            AmazonPaymentTransaction.transaction_type,
            func.count().label("rows"),
            func.coalesce(func.sum(AmazonPaymentTransaction.quantity), 0).label("quantity"),
            func.coalesce(func.sum(AmazonPaymentTransaction.product_charges), 0).label("revenue_original"),
            func.coalesce(func.sum(AmazonPaymentTransaction.promotional_rebates), 0).label("promotional_rebates"),
            func.coalesce(func.sum(AmazonPaymentTransaction.amazon_fees), 0).label("amazon_fees"),
            func.coalesce(func.sum(AmazonPaymentTransaction.other_amount), 0).label("other_amount"),
        )
        .where(AmazonPaymentTransaction.product_details.is_not(None))
        .where(AmazonPaymentTransaction.product_details != "")
    )
    transaction_query = apply_date_filters(transaction_query, start_date, end_date)
    transaction_query = transaction_query.group_by(
        AmazonPaymentTransaction.product_details,
        AmazonPaymentTransaction.sku,
        AmazonPaymentTransaction.external_transaction_id,
        AmazonPaymentTransaction.transaction_date,
        AmazonPaymentTransaction.marketplace,
        AmazonPaymentTransaction.fulfillment_channel,
        AmazonPaymentTransaction.currency,
        AmazonPaymentTransaction.transaction_type,
    )
    transaction_rows = list((await db.execute(transaction_query)).all())

    order_items = await db.scalars(select(AmazonOrderItem))
    order_by_payment_key = {
        (item.amazon_order_id, item.sku): item
        for item in order_items
    }

    by_product: dict[tuple[str, str, str], dict[str, object]] = {}
    sold_keys_by_sku: dict[str, list[tuple[str, str, str]]] = {}
    applied_fifo_events: set[tuple[str, str]] = set()

    def add_transaction_to_bucket(
        row: object,
        category: str,
        key: tuple[str, str, str],
        matched_order: AmazonOrderItem | None,
    ) -> None:
        fulfillment_channel = key[1]
        currency = key[2]
        matched_order = order_by_payment_key.get(
            (str(row.external_transaction_id or ""), str(row.sku or ""))
        ) if matched_order is None else matched_order
        bucket = by_product.setdefault(
            key,
            {
                "product_details": (
                    matched_order.product_name
                    if matched_order and matched_order.product_name
                    else row.product_details
                ),
                "sku": row.sku,
                "asin": matched_order.asin if matched_order else None,
                "marketplace": matched_order.marketplace if matched_order else row.marketplace,
                "fulfillment_channel": fulfillment_channel,
                "currency": currency,
                "transaction_rows": 0,
                "units_estimated": 0,
                "units_refunded": 0,
                "revenue_original": 0.0,
                "revenue_eur": 0.0,
                "sales_vat_eur": 0.0,
                "refunds_eur": 0.0,
                "promotional_rebates_eur": 0.0,
                "amazon_fees_eur": 0.0,
                "other_amount_eur": 0.0,
                "fx_rate_weighted": 0.0,
                "fx_rate_weight": 0.0,
                "fifo_units_costed": 0.0,
                "fifo_cogs_eur": 0.0,
                "product_details_aliases": set(),
            },
        )
        if row.product_details:
            bucket["product_details_aliases"].add(str(row.product_details))
        if matched_order and matched_order.product_name:
            bucket["product_details_aliases"].add(str(matched_order.product_name))
        if matched_order and matched_order.asin:
            bucket["asin"] = matched_order.asin
        if row.product_details and (
            not bucket.get("product_details")
            or len(str(row.product_details)) > len(str(bucket.get("product_details") or ""))
        ):
            bucket["product_details"] = row.product_details
        rate_to_eur = get_rate_on_date(
            fx_history,
            row.currency,
            row.transaction_date,
        )
        fx_weight = abs(money(row.revenue_original)) or abs(money(row.amazon_fees)) or 1
        bucket["fx_rate_weighted"] = (
            float(bucket["fx_rate_weighted"]) + money(rate_to_eur) * fx_weight
        )
        bucket["fx_rate_weight"] = float(bucket["fx_rate_weight"]) + fx_weight
        bucket["transaction_rows"] = int(bucket["transaction_rows"]) + int(row.rows)
        quantity = money(row.quantity)
        if category == "order" or is_order_payment(row.transaction_type):
            bucket["revenue_original"] = round(float(bucket["revenue_original"]) + money(row.revenue_original), 2)
            bucket["revenue_eur"] = round(
                float(bucket["revenue_eur"]) + eur(row.revenue_original, rate_to_eur),
                2,
            )
            order_quantity = money(matched_order.quantity) if matched_order else 0.0
            bucket["units_estimated"] = int(bucket["units_estimated"]) + int(
                order_quantity if matched_order else (quantity if quantity else row.rows)
            )
            if matched_order:
                order_currency = matched_order.currency or row.currency or "EUR"
                order_rate_to_eur = get_rate_on_date(
                    fx_history,
                    order_currency,
                    row.transaction_date,
                )
                bucket["sales_vat_eur"] = round(
                    float(bucket["sales_vat_eur"])
                    + eur(matched_order.item_tax + matched_order.shipping_tax, order_rate_to_eur),
                    2,
                )
            fifo_key = (
                str(row.external_transaction_id or ""),
                str(row.sku or ""),
            )
            fifo_cost = fifo_costs.get(fifo_key)
            if fifo_cost and fifo_key not in applied_fifo_events:
                bucket["fifo_units_costed"] = round(
                    float(bucket["fifo_units_costed"]) + float(fifo_cost.units),
                    3,
                )
                bucket["fifo_cogs_eur"] = round(
                    float(bucket["fifo_cogs_eur"]) + float(fifo_cost.cogs_eur),
                    2,
                )
                applied_fifo_events.add(fifo_key)
        elif category == "refund":
            bucket["refunds_eur"] = round(
                float(bucket["refunds_eur"]) + eur(row.revenue_original, rate_to_eur),
                2,
            )
            bucket["units_refunded"] = int(bucket["units_refunded"]) + int(abs(quantity) if quantity else row.rows)
        bucket["promotional_rebates_eur"] = round(
            float(bucket["promotional_rebates_eur"]) + eur(row.promotional_rebates, rate_to_eur),
            2,
        )
        bucket["amazon_fees_eur"] = round(
            float(bucket["amazon_fees_eur"]) + eur(row.amazon_fees, rate_to_eur),
            2,
        )
        bucket["other_amount_eur"] = round(
            float(bucket["other_amount_eur"]) + eur(row.other_amount, rate_to_eur),
            2,
        )

    # First create product rows only from actual order payments. This prevents
    # transfers, storage fees, return fees, and other ledger rows from becoming
    # fake products in Product Profitability.
    for row in transaction_rows:
        category = classify_payment_type(row.transaction_type)
        if category != "order":
            continue
        matched_order = order_by_payment_key.get(
            (str(row.external_transaction_id or ""), str(row.sku or ""))
        )
        fulfillment_channel = (
            matched_order.fulfillment_channel
            if matched_order
            else row.fulfillment_channel
        )
        currency = (
            matched_order.currency
            if matched_order and matched_order.currency
            else row.currency
        )
        key = (row.sku or row.product_details, fulfillment_channel, currency)
        add_transaction_to_bucket(row, category, key, matched_order)
        if row.sku:
            sku_keys = sold_keys_by_sku.setdefault(str(row.sku), [])
            if key not in sku_keys:
                sku_keys.append(key)

    # Refunds are product-level only when their SKU can be attached to a
    # product sold in the selected period. Return/FBA/service fees and transfers
    # remain in Amazon P&L until a reliable product mapping exists.
    for row in transaction_rows:
        category = classify_payment_type(row.transaction_type)
        if category != "refund" or not row.sku:
            continue
        matched_order = order_by_payment_key.get(
            (str(row.external_transaction_id or ""), str(row.sku or ""))
        )
        candidate_keys = sold_keys_by_sku.get(str(row.sku), [])
        preferred_key = None
        if matched_order:
            preferred_key = (
                str(row.sku),
                matched_order.fulfillment_channel,
                matched_order.currency or row.currency,
            )
        if preferred_key not in by_product:
            preferred_key = next(
                (
                    key
                    for key in candidate_keys
                    if key[1] == row.fulfillment_channel and key[2] == row.currency
                ),
                candidate_keys[0] if len(candidate_keys) == 1 else None,
            )
        if preferred_key is None:
            continue
        add_transaction_to_bucket(row, category, preferred_key, matched_order)

    latest_costs = await db.scalars(
        select(ProductCost).order_by(ProductCost.product_name, ProductCost.effective_date.desc(), ProductCost.id.desc())
    )
    cost_by_name: dict[str, ProductCost] = {}
    cost_by_sku: dict[str, ProductCost] = {}
    cost_candidates: list[tuple[str, ProductCost]] = []
    for cost in latest_costs:
        cost_by_sku.setdefault(cost.sku, cost)
        if cost.product_name:
            cost_by_name.setdefault(cost.product_name, cost)
            cost_candidates.append((cost.product_name, cost))

    invoice_line_rows = await db.scalars(
        select(PurchaseInvoiceLine)
        .where(PurchaseInvoiceLine.line_type == "product")
        .order_by(PurchaseInvoiceLine.created_at.desc(), PurchaseInvoiceLine.id.desc())
    )
    invoice_line_candidates: list[tuple[str, PurchaseInvoiceLine]] = [
        (line.product_name, line)
        for line in invoice_line_rows
        if line.product_name
    ]

    mapping_rows = await db.scalars(select(ProductMapping).order_by(ProductMapping.id.desc()))
    mapping_by_product: dict[str, ProductMapping] = {}
    mapping_candidates: list[tuple[str, ProductMapping]] = []
    for mapping in mapping_rows:
        mapping_by_product.setdefault(mapping.amazon_product_details, mapping)
        mapping_candidates.append((mapping.amazon_product_details, mapping))

    mapping_cost_rows = await db.execute(
        select(ProductMapping, ProductCost)
        .join(PurchaseInvoiceLine, PurchaseInvoiceLine.id == ProductMapping.invoice_line_id)
        .join(ProductCost, ProductCost.product_name == PurchaseInvoiceLine.product_name)
        .order_by(
            ProductMapping.amazon_product_details,
            ProductCost.effective_date.desc(),
            ProductCost.id.desc(),
        )
    )
    cost_by_mapping: dict[str, ProductCost] = {}
    sku_by_mapping: dict[str, str | None] = {}
    ean_by_mapping: dict[str, str | None] = {}
    for mapping, cost in mapping_cost_rows:
        cost_by_mapping.setdefault(mapping.amazon_product_details, cost)
        sku_by_mapping.setdefault(mapping.amazon_product_details, mapping.sku or mapping.supplier_sku)
        ean_by_mapping.setdefault(mapping.amazon_product_details, mapping.ean)

    rows: list[ProductProfitabilityRow] = []
    for bucket in by_product.values():
        product_details = str(bucket["product_details"])
        product_details_aliases = bucket.get("product_details_aliases")
        if not isinstance(product_details_aliases, set):
            product_details_aliases = {product_details}
        tx_sku = str(bucket.get("sku") or "") or None
        mapping = mapping_by_product.get(product_details) or best_product_alias_match(product_details_aliases, mapping_candidates)
        invoice_line = best_product_alias_match(product_details_aliases, invoice_line_candidates)
        cost = (
            (cost_by_sku.get(tx_sku) if tx_sku else None)
            or cost_by_name.get(product_details)
            or cost_by_mapping.get(product_details)
            or (cost_by_mapping.get(mapping.amazon_product_details) if isinstance(mapping, ProductMapping) else None)
            or best_product_alias_match(product_details_aliases, cost_candidates, min_score=Decimal("55"))
        )
        sku = (
            tx_sku
            or sku_by_mapping.get(product_details)
            or (mapping.sku or mapping.supplier_sku if isinstance(mapping, ProductMapping) else None)
            or (invoice_line.sku or invoice_line.supplier_sku if isinstance(invoice_line, PurchaseInvoiceLine) else None)
            or (cost.sku if cost else None)
        )
        asin = str(bucket.get("asin") or "") or None
        ean = (
            ean_by_mapping.get(product_details)
            or (mapping.ean if isinstance(mapping, ProductMapping) else None)
            or (invoice_line.ean if isinstance(invoice_line, PurchaseInvoiceLine) else None)
        )
        if ean is None and cost:
            asin = asin or raw_lookup(cost.raw_row, "asin", "ASIN")
            ean = raw_lookup(cost.raw_row, "ean", "EAN") or raw_lookup(cost.raw_row.get("raw_row"), "ean", "EAN")
        elif cost:
            asin = asin or raw_lookup(cost.raw_row, "asin", "ASIN")
        units_estimated = int(bucket["units_estimated"])
        fifo_units_costed = float(bucket["fifo_units_costed"])
        fifo_cogs_eur = round(float(bucket["fifo_cogs_eur"]), 2)
        has_complete_fifo_cost = (
            units_estimated > 0
            and abs(fifo_units_costed - units_estimated) <= 0.001
        )
        purchase_cost_eur = (
            round(fifo_cogs_eur / units_estimated, 2)
            if has_complete_fifo_cost
            else None
        )
        units_refunded = int(bucket["units_refunded"])
        revenue_eur = float(bucket["revenue_eur"])
        sales_vat_eur = round(float(bucket["sales_vat_eur"]), 2)
        revenue_gross_eur = round(revenue_eur + sales_vat_eur, 2)
        refunds_eur = float(bucket["refunds_eur"])
        promotional_rebates_eur = float(bucket["promotional_rebates_eur"])
        amazon_fees_eur = float(bucket["amazon_fees_eur"])
        other_amount_eur = float(bucket["other_amount_eur"])
        fulfillment_channel = str(bucket["fulfillment_channel"]).upper()
        if fulfillment_channel == "FBA":
            prep_cost_eur = round(
                units_estimated * fulfillment_costs["fba_prep_per_unit"],
                2,
            )
            storage_cost_eur = round(
                units_estimated * fulfillment_costs["fba_storage_per_unit"],
                2,
            )
            fbm_logistics_cost_eur = 0.0
        elif fulfillment_channel == "FBM":
            prep_cost_eur = round(
                units_estimated * fulfillment_costs["fbm_prep_per_unit"],
                2,
            )
            storage_cost_eur = round(
                units_estimated * fulfillment_costs["fbm_storage_per_unit"],
                2,
            )
            fbm_logistics_cost_eur = round(
                units_estimated
                * (
                    fulfillment_costs["fbm_packaging_per_unit"]
                    + fulfillment_costs["fbm_outbound_per_unit"]
                ),
                2,
            )
        else:
            prep_cost_eur = 0.0
            storage_cost_eur = 0.0
            fbm_logistics_cost_eur = 0.0
        operational_cost_eur = round(
            prep_cost_eur + storage_cost_eur + fbm_logistics_cost_eur,
            2,
        )
        fx_rate_weight = float(bucket["fx_rate_weight"])
        effective_fx_rate = (
            round(float(bucket["fx_rate_weighted"]) / fx_rate_weight, 8)
            if fx_rate_weight
            else money(get_rate_for_currency(rates, str(bucket["currency"])))
        )
        average_selling_price_eur = (
            round(revenue_eur / units_estimated, 2)
            if units_estimated
            else None
        )
        cogs_eur = fifo_cogs_eur if has_complete_fifo_cost else None
        gross_profit_eur = (
            round(revenue_eur - cogs_eur, 2)
            if cogs_eur is not None
            else None
        )
        net_profit_eur = (
            round(
                revenue_eur
                + refunds_eur
                + promotional_rebates_eur
                + amazon_fees_eur
                + other_amount_eur
                - operational_cost_eur
                - cogs_eur,
                2,
            )
            if cogs_eur is not None
            else None
        )
        margin_percent = (
            round((gross_profit_eur / revenue_eur) * 100, 2)
            if revenue_eur and gross_profit_eur is not None
            else None
        )
        roi_percent = (
            round((gross_profit_eur / cogs_eur) * 100, 2)
            if cogs_eur and gross_profit_eur is not None
            else None
        )
        net_margin_percent = (
            round((net_profit_eur / revenue_eur) * 100, 2)
            if revenue_eur and net_profit_eur is not None
            else None
        )
        net_roi_percent = (
            round((net_profit_eur / cogs_eur) * 100, 2)
            if cogs_eur and net_profit_eur is not None
            else None
        )
        status = profitability_status(net_profit_eur)
        rows.append(
            ProductProfitabilityRow(
                product_details=product_details,
                asin=asin,
                sku=sku,
                ean=ean,
                fulfillment_channel=str(bucket["fulfillment_channel"]),
                currency=str(bucket["currency"]),
                fx_rate_to_eur=effective_fx_rate,
                transaction_rows=int(bucket["transaction_rows"]),
                units_estimated=units_estimated,
                units_refunded=units_refunded,
                revenue_original=float(bucket["revenue_original"]),
                revenue_gross_eur=revenue_gross_eur,
                sales_vat_eur=sales_vat_eur,
                revenue_eur=revenue_eur,
                refunds_eur=refunds_eur,
                promotional_rebates_eur=promotional_rebates_eur,
                amazon_fees_eur=amazon_fees_eur,
                other_amount_eur=other_amount_eur,
                prep_cost_eur=prep_cost_eur,
                storage_cost_eur=storage_cost_eur,
                fbm_logistics_cost_eur=fbm_logistics_cost_eur,
                operational_cost_eur=operational_cost_eur,
                average_selling_price_eur=average_selling_price_eur,
                purchase_cost_eur=purchase_cost_eur,
                cogs_eur=cogs_eur,
                gross_profit_eur=gross_profit_eur,
                net_profit_eur=net_profit_eur,
                margin_percent=margin_percent,
                roi_percent=roi_percent,
                net_margin_percent=net_margin_percent,
                net_roi_percent=net_roi_percent,
                profitability_status=status,
                cost_match_status="matched" if has_complete_fifo_cost else "missing_cost",
            )
        )

    rows.sort(key=lambda item: item.net_profit_eur if item.net_profit_eur is not None else -999999, reverse=True)
    matched_rows = [row for row in rows if row.cost_match_status == "matched"]
    revenue_gross_eur = round(sum(row.revenue_gross_eur for row in rows), 2)
    sales_vat_eur = round(sum(row.sales_vat_eur for row in rows), 2)
    revenue_eur = round(sum(row.revenue_eur for row in rows), 2)
    refunds_eur = round(sum(row.refunds_eur for row in rows), 2)
    promotional_rebates_eur = round(sum(row.promotional_rebates_eur for row in rows), 2)
    amazon_fees_eur = round(sum(row.amazon_fees_eur for row in rows), 2)
    other_amount_eur = round(sum(row.other_amount_eur for row in rows), 2)
    operational_cost_eur = round(sum(row.operational_cost_eur for row in rows), 2)
    cogs_eur = round(sum(row.cogs_eur or 0 for row in matched_rows), 2)
    gross_profit_eur = round(sum(row.gross_profit_eur or 0 for row in matched_rows), 2)
    net_profit_eur = round(sum(row.net_profit_eur or 0 for row in matched_rows), 2)
    matched_revenue_eur = round(sum(row.revenue_eur for row in matched_rows), 2)
    margin_percent = round((gross_profit_eur / matched_revenue_eur) * 100, 2) if matched_revenue_eur else None
    roi_percent = round((gross_profit_eur / cogs_eur) * 100, 2) if cogs_eur else None
    net_margin_percent = round((net_profit_eur / matched_revenue_eur) * 100, 2) if matched_revenue_eur else None
    net_roi_percent = round((net_profit_eur / cogs_eur) * 100, 2) if cogs_eur else None
    return ProductProfitabilityResponse(
        summary=ProductProfitabilitySummary(
            products=len(rows),
            matched_products=len(matched_rows),
            missing_cost_products=len(rows) - len(matched_rows),
            units_estimated=sum(row.units_estimated for row in rows),
            units_refunded=sum(row.units_refunded for row in rows),
            revenue_gross_eur=revenue_gross_eur,
            sales_vat_eur=sales_vat_eur,
            revenue_eur=revenue_eur,
            refunds_eur=refunds_eur,
            promotional_rebates_eur=promotional_rebates_eur,
            amazon_fees_eur=amazon_fees_eur,
            other_amount_eur=other_amount_eur,
            operational_cost_eur=operational_cost_eur,
            cogs_eur=cogs_eur,
            gross_profit_eur=gross_profit_eur,
            net_profit_eur=net_profit_eur,
            margin_percent=margin_percent,
            roi_percent=roi_percent,
            net_margin_percent=net_margin_percent,
            net_roi_percent=net_roi_percent,
            profitable_products=sum(1 for row in matched_rows if row.profitability_status == "profitable"),
            loss_products=sum(1 for row in matched_rows if row.profitability_status == "loss"),
            breakeven_products=sum(1 for row in matched_rows if row.profitability_status == "breakeven"),
        ),
        rows=rows[:limit],
    )


@router.get("/purchase-summary", response_model=PurchaseSummaryResponse)
async def purchase_summary(
    db: Annotated[AsyncSession, Depends(get_db)],
    start_date: Annotated[date | None, Query()] = None,
    end_date: Annotated[date | None, Query()] = None,
) -> PurchaseSummaryResponse:
    group_by_month = bool(start_date or end_date)
    month_expr = (
        func.date_trunc("month", PurchaseInvoice.invoice_date).label("month")
        if group_by_month
        else literal(None).label("month")
    )
    total_expr = func.coalesce(
        PurchaseInvoiceLine.line_gross_amount,
        PurchaseInvoiceLine.line_net_amount + func.coalesce(PurchaseInvoiceLine.vat_amount, 0),
        PurchaseInvoiceLine.line_net_amount,
        0,
    )
    query = (
        select(
            month_expr,
            PurchaseInvoice.supplier_name,
            PurchaseInvoice.currency,
            func.count(func.distinct(PurchaseInvoice.id)).label("invoices"),
            func.count(PurchaseInvoiceLine.id).label("lines"),
            func.coalesce(func.sum(case((PurchaseInvoiceLine.line_type == "product", 1), else_=0)), 0).label("product_lines"),
            func.coalesce(func.sum(case((PurchaseInvoiceLine.line_type != "product", 1), else_=0)), 0).label("expense_lines"),
            func.coalesce(func.sum(case((PurchaseInvoiceLine.line_type == "product", PurchaseInvoiceLine.quantity), else_=0)), 0).label("quantity"),
            func.coalesce(func.sum(PurchaseInvoiceLine.line_net_amount), 0).label("subtotal_amount"),
            func.coalesce(func.sum(case((PurchaseInvoiceLine.line_type == "product", PurchaseInvoiceLine.line_net_amount), else_=0)), 0).label("product_subtotal_amount"),
            func.coalesce(func.sum(case((PurchaseInvoiceLine.line_type != "product", PurchaseInvoiceLine.line_net_amount), else_=0)), 0).label("expense_subtotal_amount"),
            func.coalesce(func.sum(case((PurchaseInvoiceLine.line_type == "inbound_shipping", PurchaseInvoiceLine.line_net_amount), else_=0)), 0).label("inbound_shipping_amount"),
            func.coalesce(func.sum(case((PurchaseInvoiceLine.line_type == "fulfillment_fee", PurchaseInvoiceLine.line_net_amount), else_=0)), 0).label("fulfillment_fee_amount"),
            func.coalesce(func.sum(case((PurchaseInvoiceLine.line_type == "marketplace_fee", PurchaseInvoiceLine.line_net_amount), else_=0)), 0).label("marketplace_fee_amount"),
            func.coalesce(func.sum(case((PurchaseInvoiceLine.line_type.in_(("service", "other")), PurchaseInvoiceLine.line_net_amount), else_=0)), 0).label("other_service_amount"),
            func.coalesce(func.sum(PurchaseInvoiceLine.vat_amount), 0).label("vat_amount"),
            func.coalesce(func.sum(total_expr), 0).label("total_amount"),
        )
        .join(PurchaseInvoiceLine, PurchaseInvoiceLine.invoice_id == PurchaseInvoice.id)
    )
    query = apply_invoice_date_filters(query, start_date, end_date)
    query = query.group_by(PurchaseInvoice.supplier_name, PurchaseInvoice.currency)
    if group_by_month:
        query = query.group_by(month_expr).order_by(month_expr.desc(), PurchaseInvoice.supplier_name)
    else:
        query = query.order_by(PurchaseInvoice.supplier_name)
    result = await db.execute(query)
    return PurchaseSummaryResponse(
        rows=[
            PurchaseSummaryRow(
                month=row.month.date().isoformat() if row.month else "all",
                supplier_name=row.supplier_name,
                currency=row.currency,
                invoices=row.invoices,
                lines=row.lines,
                product_lines=row.product_lines,
                expense_lines=row.expense_lines,
                quantity=float(row.quantity or 0),
                subtotal_amount=money(row.subtotal_amount),
                product_subtotal_amount=money(row.product_subtotal_amount),
                expense_subtotal_amount=money(row.expense_subtotal_amount),
                inbound_shipping_amount=money(row.inbound_shipping_amount),
                fulfillment_fee_amount=money(row.fulfillment_fee_amount),
                marketplace_fee_amount=money(row.marketplace_fee_amount),
                other_service_amount=money(row.other_service_amount),
                vat_amount=money(row.vat_amount),
                total_amount=money(row.total_amount),
            )
            for row in result
        ]
    )
