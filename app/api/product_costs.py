from datetime import date, datetime
from decimal import Decimal
import hashlib
from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile
from pydantic import BaseModel, Field
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.ingestion.product_costs import build_product_cost_preview
from app.models.product_cost import ProductCost
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


class ProductCostLineRow(BaseModel):
    id: int
    import_id: int
    sku: str
    ean: str | None
    product_name: str | None
    purchase_cost: float
    currency: str
    effective_date: str
    source_filename: str | None = None


class ProductCostLineListResponse(BaseModel):
    rows: list[ProductCostLineRow]


class ProductCostManualRequest(BaseModel):
    sku: str = Field(min_length=1, max_length=120)
    ean: str | None = None
    product_name: str | None = None
    purchase_cost: float = Field(gt=0)
    currency: str = Field(default="EUR", min_length=3, max_length=8)
    effective_date: date


class ProductCostUpdateRequest(BaseModel):
    sku: str = Field(min_length=1, max_length=120)
    ean: str | None = None
    product_name: str | None = None
    purchase_cost: float = Field(gt=0)
    currency: str = Field(default="EUR", min_length=3, max_length=8)
    effective_date: date


class DeleteProductCostImportResponse(BaseModel):
    import_id: int
    deleted: bool


def cost_row(row: ProductCost, source_filename: str | None = None) -> ProductCostLineRow:
    raw_row = row.raw_row or {}
    ean = raw_row.get("ean") or raw_row.get("EAN") or raw_row.get("raw_row", {}).get("EAN")
    return ProductCostLineRow(
        id=row.id,
        import_id=row.import_id,
        sku=row.sku,
        ean=str(ean) if ean else None,
        product_name=row.product_name,
        purchase_cost=float(row.purchase_cost),
        currency=row.currency,
        effective_date=row.effective_date.isoformat(),
        source_filename=source_filename,
    )


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


@router.get("/lines", response_model=ProductCostLineListResponse)
async def list_product_cost_lines(
    db: Annotated[AsyncSession, Depends(get_db)],
    limit: int = 500,
) -> ProductCostLineListResponse:
    result = await db.execute(
        select(ProductCost, ProductCostImport.source_filename)
        .join(ProductCostImport, ProductCostImport.id == ProductCost.import_id)
        .order_by(ProductCost.effective_date.desc(), ProductCost.id.desc())
        .limit(limit)
    )
    return ProductCostLineListResponse(
        rows=[cost_row(row, source_filename) for row, source_filename in result]
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
    start_date: Annotated[date | None, Query()] = None,
    end_date: Annotated[date | None, Query()] = None,
) -> ProductCostImportListResponse:
    statement = select(ProductCostImport).where(~ProductCostImport.source_filename.ilike("invoice_costs_%"))
    if start_date:
        statement = statement.where(ProductCostImport.effective_date >= start_date)
    if end_date:
        statement = statement.where(ProductCostImport.effective_date <= end_date)
    result = await db.scalars(statement.order_by(ProductCostImport.created_at.desc()))
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


@router.post("/manual", response_model=ProductCostLineRow)
async def create_manual_product_cost(
    payload: ProductCostManualRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ProductCostLineRow:
    fingerprint = hashlib.sha256(
        f"manual:{payload.sku}:{payload.effective_date}:{datetime.utcnow().isoformat()}".encode()
    ).hexdigest()
    cost_import = ProductCostImport(
        source_filename=f"manual_cost_{payload.sku}_{payload.effective_date}.json",
        source_sha256=fingerprint,
        currency=payload.currency.upper(),
        effective_date=payload.effective_date,
        header_mapping={
            "sku": "manual.sku",
            "ean": "manual.ean",
            "product_name": "manual.product_name",
            "purchase_cost": "manual.purchase_cost",
        },
        row_count=1,
    )
    db.add(cost_import)
    await db.flush()
    cost = ProductCost(
        import_id=cost_import.id,
        sku=payload.sku.strip(),
        product_name=(payload.product_name or "").strip() or None,
        purchase_cost=Decimal(str(payload.purchase_cost)),
        currency=payload.currency.upper(),
        effective_date=payload.effective_date,
        raw_row={
            "source": "manual",
            "ean": (payload.ean or "").strip() or None,
        },
    )
    db.add(cost)
    await db.commit()
    await db.refresh(cost)
    return cost_row(cost, cost_import.source_filename)


@router.put("/lines/{cost_id}", response_model=ProductCostLineRow)
async def update_product_cost_line(
    cost_id: int,
    payload: ProductCostUpdateRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ProductCostLineRow:
    cost = await db.get(ProductCost, cost_id)
    if cost is None:
        raise HTTPException(status_code=404, detail="Product cost was not found.")
    cost.sku = payload.sku.strip()
    cost.product_name = (payload.product_name or "").strip() or None
    cost.purchase_cost = Decimal(str(payload.purchase_cost))
    cost.currency = payload.currency.upper()
    cost.effective_date = payload.effective_date
    raw_row = dict(cost.raw_row or {})
    raw_row["ean"] = (payload.ean or "").strip() or None
    cost.raw_row = raw_row
    await db.commit()
    await db.refresh(cost)
    cost_import = await db.get(ProductCostImport, cost.import_id)
    return cost_row(cost, cost_import.source_filename if cost_import else None)


@router.delete("/{import_id:int}", response_model=DeleteProductCostImportResponse)
async def delete_product_cost_import(
    import_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> DeleteProductCostImportResponse:
    cost_import = await db.get(ProductCostImport, import_id)
    if cost_import is None or cost_import.source_filename.startswith("invoice_costs_"):
        raise HTTPException(status_code=404, detail="Product cost import not found.")
    await db.execute(delete(ProductCost).where(ProductCost.import_id == import_id))
    await db.delete(cost_import)
    await db.commit()
    return DeleteProductCostImportResponse(import_id=import_id, deleted=True)


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
