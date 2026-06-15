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
from app.services.fx import convert_to_eur_with_rate, get_latest_fx_rates, get_rate_for_currency
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


class DataQualitySummary(BaseModel):
    payment_rows: int
    rows_with_sku: int
    rows_without_sku: int
    sold_skus: int
    missing_cost_skus: int
    unknown_transaction_types: int


class DataQualityResponse(BaseModel):
    start_date: str | None
    end_date: str | None
    summary: DataQualitySummary
    missing_costs: list[MissingCostRow]
    unknown_transaction_types: list[UnknownTransactionTypeRow]


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
    month_expr = func.date_trunc("month", AmazonPaymentTransaction.transaction_date).label("month")
    query = select(
        month_expr,
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
        month_expr,
        AmazonPaymentTransaction.marketplace,
        AmazonPaymentTransaction.currency,
        AmazonPaymentTransaction.transaction_type,
    ).order_by(month_expr, AmazonPaymentTransaction.marketplace, AmazonPaymentTransaction.transaction_type)

    result = await db.execute(query)
    rates = await get_latest_fx_rates(db)
    rows = []
    for row in result:
        rate_to_eur = get_rate_for_currency(rates, row.currency)
        rows.append(
            PaymentSummaryRow(
                month=row.month.date().isoformat(),
                marketplace=row.marketplace,
                currency=row.currency,
                fx_rate_to_eur=money(rate_to_eur),
                transaction_type=row.transaction_type,
                rows=row.rows,
                product_charges=money(row.product_charges),
                promotional_rebates=money(row.promotional_rebates),
                amazon_fees=money(row.amazon_fees),
                other_amount=money(row.other_amount),
                total_amount=money(row.total_amount),
                product_charges_eur=eur(row.product_charges, rate_to_eur),
                promotional_rebates_eur=eur(row.promotional_rebates, rate_to_eur),
                amazon_fees_eur=eur(row.amazon_fees, rate_to_eur),
                other_amount_eur=eur(row.other_amount, rate_to_eur),
                total_amount_eur=eur(row.total_amount, rate_to_eur),
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
        AmazonPaymentTransaction.transaction_type,
        AmazonPaymentTransaction.fulfillment_channel,
        AmazonPaymentTransaction.currency,
    ).order_by(
        AmazonPaymentTransaction.transaction_type,
        AmazonPaymentTransaction.fulfillment_channel,
        AmazonPaymentTransaction.currency,
    )
    result = await db.execute(query)
    rates = await get_latest_fx_rates(db)

    rows: list[AmazonPnlCategoryRow] = []
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
        rate_to_eur = get_rate_for_currency(rates, row.currency)
        product_charges_eur = eur(row.product_charges, rate_to_eur)
        promotional_rebates_eur = eur(row.promotional_rebates, rate_to_eur)
        amazon_fees_eur = eur(row.amazon_fees, rate_to_eur)
        other_amount_eur = eur(row.other_amount, rate_to_eur)
        total_amount_eur = eur(row.total_amount, rate_to_eur)
        quantity = money(row.quantity)
        rows.append(
            AmazonPnlCategoryRow(
                category=category,
                transaction_type=row.transaction_type,
                fulfillment_channel=row.fulfillment_channel,
                rows=int(row.rows),
                units=quantity,
                product_charges_eur=product_charges_eur,
                promotional_rebates_eur=promotional_rebates_eur,
                amazon_fees_eur=amazon_fees_eur,
                other_amount_eur=other_amount_eur,
                total_amount_eur=total_amount_eur,
            )
        )
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
        ),
        missing_costs=missing_costs[:limit],
        unknown_transaction_types=unknown_types[:limit],
    )


@router.get("/product-profitability", response_model=ProductProfitabilityResponse)
async def product_profitability(
    db: Annotated[AsyncSession, Depends(get_db)],
    limit: Annotated[int, Query(ge=1, le=10000)] = 5000,
    start_date: Annotated[date | None, Query()] = None,
    end_date: Annotated[date | None, Query()] = None,
) -> ProductProfitabilityResponse:
    rates = await get_latest_fx_rates(db)

    transaction_query = (
        select(
            AmazonPaymentTransaction.product_details,
            AmazonPaymentTransaction.sku,
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
        AmazonPaymentTransaction.fulfillment_channel,
        AmazonPaymentTransaction.currency,
        AmazonPaymentTransaction.transaction_type,
    )
    transaction_rows = await db.execute(transaction_query)

    by_product: dict[tuple[str, str], dict[str, float | int | str]] = {}
    for row in transaction_rows:
        category = classify_payment_type(row.transaction_type)
        key = (row.sku or row.product_details, row.fulfillment_channel, row.currency)
        bucket = by_product.setdefault(
            key,
            {
                "product_details": row.product_details,
                "sku": row.sku,
                "fulfillment_channel": row.fulfillment_channel,
                "currency": row.currency,
                "transaction_rows": 0,
                "units_estimated": 0,
                "units_refunded": 0,
                "revenue_original": 0.0,
                "revenue_eur": 0.0,
                "refunds_eur": 0.0,
                "promotional_rebates_eur": 0.0,
                "amazon_fees_eur": 0.0,
                "other_amount_eur": 0.0,
                "product_details_aliases": set(),
            },
        )
        if row.product_details:
            bucket["product_details_aliases"].add(str(row.product_details))
        if row.product_details and (
            not bucket.get("product_details")
            or len(str(row.product_details)) > len(str(bucket.get("product_details") or ""))
        ):
            bucket["product_details"] = row.product_details
        rate_to_eur = get_rate_for_currency(rates, row.currency)
        bucket["transaction_rows"] = int(bucket["transaction_rows"]) + int(row.rows)
        quantity = money(row.quantity)
        if category == "order" or is_order_payment(row.transaction_type):
            bucket["revenue_original"] = round(float(bucket["revenue_original"]) + money(row.revenue_original), 2)
            bucket["revenue_eur"] = round(
                float(bucket["revenue_eur"]) + eur(row.revenue_original, rate_to_eur),
                2,
            )
            bucket["units_estimated"] = int(bucket["units_estimated"]) + int(quantity if quantity else row.rows)
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

    order_tax_query = (
        select(
            AmazonOrderItem.sku,
            AmazonOrderItem.fulfillment_channel,
            AmazonOrderItem.currency,
            func.coalesce(func.sum(AmazonOrderItem.item_tax + AmazonOrderItem.shipping_tax), 0).label("sales_vat"),
        )
        .where(AmazonOrderItem.sku.is_not(None))
        .where(AmazonOrderItem.sku != "")
    )
    if start_date:
        order_tax_query = order_tax_query.where(func.date(AmazonOrderItem.purchase_date) >= start_date)
    if end_date:
        order_tax_query = order_tax_query.where(func.date(AmazonOrderItem.purchase_date) <= end_date)
    order_tax_query = order_tax_query.group_by(
        AmazonOrderItem.sku,
        AmazonOrderItem.fulfillment_channel,
        AmazonOrderItem.currency,
    )
    order_tax_rows = await db.execute(order_tax_query)
    sales_vat_by_key: dict[tuple[str, str, str], float] = {}
    for row in order_tax_rows:
        currency = row.currency or "EUR"
        rate_to_eur = get_rate_for_currency(rates, currency)
        sales_vat_by_key[
            (str(row.sku), str(row.fulfillment_channel), str(currency))
        ] = eur(row.sales_vat, rate_to_eur)

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
        asin = None
        ean = (
            ean_by_mapping.get(product_details)
            or (mapping.ean if isinstance(mapping, ProductMapping) else None)
            or (invoice_line.ean if isinstance(invoice_line, PurchaseInvoiceLine) else None)
        )
        if ean is None and cost:
            asin = raw_lookup(cost.raw_row, "asin", "ASIN")
            ean = raw_lookup(cost.raw_row, "ean", "EAN") or raw_lookup(cost.raw_row.get("raw_row"), "ean", "EAN")
        elif cost:
            asin = raw_lookup(cost.raw_row, "asin", "ASIN")
        purchase_cost_eur = money(cost.purchase_cost) if cost else None
        units_estimated = int(bucket["units_estimated"])
        units_refunded = int(bucket["units_refunded"])
        revenue_gross_eur = float(bucket["revenue_eur"])
        sales_vat_eur = round(
            sales_vat_by_key.get(
                (
                    str(sku or ""),
                    str(bucket["fulfillment_channel"]),
                    str(bucket["currency"] or "EUR"),
                ),
                0.0,
            ),
            2,
        )
        revenue_eur = round(revenue_gross_eur - sales_vat_eur, 2)
        refunds_eur = float(bucket["refunds_eur"])
        promotional_rebates_eur = float(bucket["promotional_rebates_eur"])
        amazon_fees_eur = float(bucket["amazon_fees_eur"])
        other_amount_eur = float(bucket["other_amount_eur"])
        average_selling_price_eur = (
            round(revenue_eur / units_estimated, 2)
            if units_estimated
            else None
        )
        cogs_eur = round(units_estimated * purchase_cost_eur, 2) if purchase_cost_eur is not None else None
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
                fx_rate_to_eur=money(get_rate_for_currency(rates, str(bucket["currency"]))),
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
                cost_match_status="matched" if cost else "missing_cost",
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
