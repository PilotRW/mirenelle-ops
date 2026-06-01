from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.models.amazon_payment_transaction import AmazonPaymentTransaction
from app.models.product_mapping import ProductMapping
from app.models.purchase_invoice import PurchaseInvoice
from app.models.purchase_invoice_line import PurchaseInvoiceLine
from app.services.transaction_classifier import is_order_payment
from app.services.product_mapping_service import (
    build_product_mapping_suggestions,
    create_product_mapping,
    product_similarity,
)
from app.services.fx import convert_to_eur_with_rate, get_latest_fx_rates, get_rate_for_currency


router = APIRouter(prefix="/product-mappings", tags=["product-mappings"])


class ProductMappingCreateRequest(BaseModel):
    invoice_line_id: int
    amazon_product_details: str = Field(min_length=1)
    confidence: float | None = None
    match_method: str = "manual"
    notes: str | None = None


class ProductMappingRow(BaseModel):
    id: int
    invoice_line_id: int
    supplier_name: str | None
    supplier_sku: str | None
    sku: str | None
    ean: str | None
    invoice_product_name: str
    amazon_product_details: str
    confidence: float | None
    match_method: str
    created_at: str


class ProductMappingListResponse(BaseModel):
    rows: list[ProductMappingRow]


class ProductMappingSuggestionRow(BaseModel):
    invoice_line_id: int
    supplier_name: str
    supplier_sku: str | None
    sku: str | None
    ean: str | None
    invoice_product_name: str
    amazon_product_details: str
    transaction_rows: int
    confidence: float


class ProductMappingSuggestionResponse(BaseModel):
    rows: list[ProductMappingSuggestionRow]


class UnmappedInvoiceLineRow(BaseModel):
    invoice_line_id: int
    supplier_name: str
    supplier_sku: str | None
    sku: str | None
    ean: str | None
    invoice_product_name: str


class UnmappedInvoiceLineResponse(BaseModel):
    rows: list[UnmappedInvoiceLineRow]


class AmazonProductSearchRow(BaseModel):
    amazon_product_details: str
    transaction_rows: int
    revenue_eur_hint: float


class AmazonProductSearchResponse(BaseModel):
    rows: list[AmazonProductSearchRow]


def mapping_row(row: ProductMapping) -> ProductMappingRow:
    return ProductMappingRow(
        id=row.id,
        invoice_line_id=row.invoice_line_id,
        supplier_name=row.supplier_name,
        supplier_sku=row.supplier_sku,
        sku=row.sku,
        ean=row.ean,
        invoice_product_name=row.invoice_product_name,
        amazon_product_details=row.amazon_product_details,
        confidence=float(row.confidence) if row.confidence is not None else None,
        match_method=row.match_method,
        created_at=row.created_at.isoformat(),
    )


@router.get("", response_model=ProductMappingListResponse)
async def list_product_mappings(
    db: Annotated[AsyncSession, Depends(get_db)],
    limit: Annotated[int, Query(ge=1, le=500)] = 100,
) -> ProductMappingListResponse:
    result = await db.scalars(
        select(ProductMapping)
        .order_by(ProductMapping.created_at.desc(), ProductMapping.id.desc())
        .limit(limit)
    )
    return ProductMappingListResponse(rows=[mapping_row(row) for row in result])


@router.get("/suggestions", response_model=ProductMappingSuggestionResponse)
async def product_mapping_suggestions(
    db: Annotated[AsyncSession, Depends(get_db)],
    limit: Annotated[int, Query(ge=1, le=200)] = 50,
    min_confidence: Annotated[float, Query(ge=0, le=100)] = 35,
) -> ProductMappingSuggestionResponse:
    suggestions = await build_product_mapping_suggestions(
        db=db,
        limit=limit,
        min_confidence=Decimal(str(min_confidence)),
    )
    return ProductMappingSuggestionResponse(
        rows=[
            ProductMappingSuggestionRow(
                invoice_line_id=row.invoice_line_id,
                supplier_name=row.supplier_name,
                supplier_sku=row.supplier_sku,
                sku=row.sku,
                ean=row.ean,
                invoice_product_name=row.invoice_product_name,
                amazon_product_details=row.amazon_product_details,
                transaction_rows=row.transaction_rows,
                confidence=float(row.confidence),
            )
            for row in suggestions
        ]
    )


@router.get("/unmapped-invoice-lines", response_model=UnmappedInvoiceLineResponse)
async def unmapped_invoice_lines(
    db: Annotated[AsyncSession, Depends(get_db)],
    query: Annotated[str | None, Query()] = None,
    limit: Annotated[int, Query(ge=1, le=500)] = 100,
) -> UnmappedInvoiceLineResponse:
    mapped_line_ids = select(ProductMapping.invoice_line_id)
    statement = (
        select(PurchaseInvoiceLine, PurchaseInvoice)
        .join(PurchaseInvoice, PurchaseInvoice.id == PurchaseInvoiceLine.invoice_id)
        .where(PurchaseInvoiceLine.line_type == "product")
        .where(PurchaseInvoiceLine.id.not_in(mapped_line_ids))
        .order_by(PurchaseInvoiceLine.created_at.desc(), PurchaseInvoiceLine.id.desc())
        .limit(limit)
    )
    if query:
        pattern = f"%{query}%"
        statement = statement.where(
            PurchaseInvoiceLine.product_name.ilike(pattern)
            | PurchaseInvoiceLine.sku.ilike(pattern)
            | PurchaseInvoiceLine.supplier_sku.ilike(pattern)
            | PurchaseInvoiceLine.ean.ilike(pattern)
        )
    result = await db.execute(statement)
    return UnmappedInvoiceLineResponse(
        rows=[
            UnmappedInvoiceLineRow(
                invoice_line_id=line.id,
                supplier_name=invoice.supplier_name,
                supplier_sku=line.supplier_sku,
                sku=line.sku,
                ean=line.ean,
                invoice_product_name=line.product_name,
            )
            for line, invoice in result
        ]
    )


@router.get("/amazon-products", response_model=AmazonProductSearchResponse)
async def amazon_products(
    db: Annotated[AsyncSession, Depends(get_db)],
    query: Annotated[str | None, Query()] = None,
    limit: Annotated[int, Query(ge=1, le=200)] = 50,
) -> AmazonProductSearchResponse:
    statement = (
        select(
            AmazonPaymentTransaction.product_details,
            AmazonPaymentTransaction.transaction_type,
            AmazonPaymentTransaction.currency,
            func.count().label("transaction_rows"),
            func.coalesce(func.sum(AmazonPaymentTransaction.product_charges), 0).label("revenue_hint"),
        )
        .where(AmazonPaymentTransaction.product_details.is_not(None))
        .where(AmazonPaymentTransaction.product_details != "")
        .group_by(
            AmazonPaymentTransaction.product_details,
            AmazonPaymentTransaction.transaction_type,
            AmazonPaymentTransaction.currency,
        )
        .order_by(func.count().desc(), AmazonPaymentTransaction.product_details)
    )
    if query:
        statement = statement.where(AmazonPaymentTransaction.product_details.ilike(f"%{query}%"))

    rates = await get_latest_fx_rates(db)
    result = await db.execute(statement)
    products: dict[str, dict[str, float | int]] = {}
    for row in result:
        if not is_order_payment(str(row.transaction_type)):
            continue
        rate_to_eur = get_rate_for_currency(rates, row.currency)
        bucket = products.setdefault(
            str(row.product_details),
            {"transaction_rows": 0, "revenue_hint": 0.0},
        )
        bucket["transaction_rows"] = int(bucket["transaction_rows"]) + int(row.transaction_rows)
        bucket["revenue_hint"] = float(bucket["revenue_hint"]) + float(convert_to_eur_with_rate(row.revenue_hint, rate_to_eur))
    rows = sorted(
        products.items(),
        key=lambda item: (-int(item[1]["transaction_rows"]), item[0]),
    )[:limit]
    return AmazonProductSearchResponse(
        rows=[
            AmazonProductSearchRow(
                amazon_product_details=product_details,
                transaction_rows=int(values["transaction_rows"]),
                revenue_eur_hint=round(float(values["revenue_hint"]), 2),
            )
            for product_details, values in rows
        ]
    )


@router.post("", response_model=ProductMappingRow)
async def create_mapping(
    payload: ProductMappingCreateRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ProductMappingRow:
    confidence = (
        Decimal(str(payload.confidence))
        if payload.confidence is not None
        else None
    )
    if confidence is None:
        # Give manual entries a useful score so reports can explain the match.
        confidence = product_similarity("", payload.amazon_product_details)
    try:
        mapping = await create_product_mapping(
            db=db,
            invoice_line_id=payload.invoice_line_id,
            amazon_product_details=payload.amazon_product_details,
            confidence=confidence,
            match_method=payload.match_method,
            notes=payload.notes,
            raw_match=payload.model_dump(),
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except IntegrityError as exc:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Product mapping already exists.") from exc
    return mapping_row(mapping)
