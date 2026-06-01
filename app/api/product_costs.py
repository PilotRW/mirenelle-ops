from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.ingestion.product_costs import build_product_cost_preview
from app.models.product_cost_import import ProductCostImport
from app.services.amazon_payment_import_service import DuplicateImportError
from app.services.product_cost_import_service import commit_product_cost_import


router = APIRouter(prefix="/imports/product-costs", tags=["product-costs"])


class ProductCostPreviewResponse(BaseModel):
    filename: str
    currency: str
    effective_date: str
    row_count: int
    parsed_row_count: int
    can_commit: bool
    headers: list[str]
    mapping: dict[str, str]
    missing_fields: list[str]
    ambiguous_headers: dict[str, list[str]]
    unknown_headers: list[str]
    validation_errors: list[str]
    sample_rows: list[dict[str, str]]
    normalized_sample_rows: list[dict[str, str | float | None]]


class ProductCostCommitResponse(BaseModel):
    import_id: int
    filename: str
    currency: str
    effective_date: str
    row_count: int
    source_sha256: str | None


class ProductCostImportRow(BaseModel):
    import_id: int
    filename: str
    currency: str
    effective_date: str
    row_count: int
    created_at: str


class ProductCostImportListResponse(BaseModel):
    rows: list[ProductCostImportRow]


def build_preview_response(preview) -> ProductCostPreviewResponse:
    return ProductCostPreviewResponse(
        filename=preview.filename,
        currency=preview.currency,
        effective_date=preview.effective_date.isoformat(),
        row_count=preview.row_count,
        parsed_row_count=len(preview.parsed_rows),
        can_commit=preview.can_commit,
        headers=preview.headers,
        mapping=preview.mapping,
        missing_fields=preview.missing_fields,
        ambiguous_headers=preview.ambiguous_headers,
        unknown_headers=preview.unknown_headers,
        validation_errors=preview.validation_errors,
        sample_rows=preview.sample_rows,
        normalized_sample_rows=preview.normalized_sample_rows,
    )


@router.post("/preview", response_model=ProductCostPreviewResponse)
async def preview_product_costs(
    file: Annotated[UploadFile, File()],
    effective_date: Annotated[date | None, Form()] = None,
    sample_size: Annotated[int, Form(ge=1, le=50)] = 10,
) -> ProductCostPreviewResponse:
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    preview = build_product_cost_preview(
        filename=file.filename or "product-costs",
        content=content,
        effective_date=effective_date,
        sample_size=sample_size,
    )
    return build_preview_response(preview)


@router.get("", response_model=ProductCostImportListResponse)
async def list_product_cost_imports(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ProductCostImportListResponse:
    result = await db.scalars(
        select(ProductCostImport)
        .where(~ProductCostImport.source_filename.ilike("invoice_costs_%"))
        .order_by(ProductCostImport.created_at.desc())
    )
    return ProductCostImportListResponse(
        rows=[
            ProductCostImportRow(
                import_id=row.id,
                filename=row.source_filename,
                currency=row.currency,
                effective_date=row.effective_date.isoformat(),
                row_count=row.row_count,
                created_at=row.created_at.isoformat(),
            )
            for row in result
        ]
    )


@router.post("/commit", response_model=ProductCostCommitResponse)
async def commit_product_costs(
    file: Annotated[UploadFile, File()],
    db: Annotated[AsyncSession, Depends(get_db)],
    effective_date: Annotated[date | None, Form()] = None,
) -> ProductCostCommitResponse:
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    preview = build_product_cost_preview(
        filename=file.filename or "product-costs",
        content=content,
        effective_date=effective_date,
        sample_size=10,
    )
    if not preview.can_commit:
        raise HTTPException(status_code=400, detail=build_preview_response(preview).model_dump())

    try:
        cost_import = await commit_product_cost_import(
            db=db,
            content=content,
            preview=preview,
        )
    except DuplicateImportError as exc:
        raise HTTPException(
            status_code=409,
            detail={"message": "File was already imported.", "import_id": exc.import_id},
        ) from exc

    return ProductCostCommitResponse(
        import_id=cost_import.id,
        filename=cost_import.source_filename,
        currency=cost_import.currency,
        effective_date=cost_import.effective_date.isoformat(),
        row_count=cost_import.row_count,
        source_sha256=cost_import.source_sha256,
    )
