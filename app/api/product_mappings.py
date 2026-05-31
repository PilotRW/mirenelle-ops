from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.models.product_mapping import ProductMapping
from app.services.product_mapping_service import (
    build_product_mapping_suggestions,
    create_product_mapping,
    product_similarity,
)


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
