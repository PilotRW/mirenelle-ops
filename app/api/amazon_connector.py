from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.settings import settings
from app.db.database import get_db
from app.ingestion.amazon_reports.order_reports import (
    REPORT_TYPE_ALL_ORDERS_BY_ORDER_DATE,
    build_order_report_preview,
)
from app.models.amazon_order_import import AmazonOrderImport
from app.models.amazon_order_item import AmazonOrderItem
from app.services.amazon_order_import_service import commit_order_report_import
from app.services.amazon_payment_import_service import DuplicateImportError


router = APIRouter(prefix="/integrations/amazon-sp-api", tags=["amazon-sp-api"])


class AmazonConnectorStatusResponse(BaseModel):
    configured: bool
    missing_settings: list[str]
    endpoint: str
    region: str
    phase_1_report_type: str


class AmazonOrderPreviewResponse(BaseModel):
    filename: str
    marketplace: str
    report_type: str
    encoding: str
    delimiter: str
    row_count: int
    can_commit: bool
    headers: list[str]
    mapping: dict[str, str]
    missing_fields: list[str]
    unknown_headers: list[str]
    totals: dict[str, float | int]
    validation_errors: list[str]
    sample_rows: list[dict[str, str]]


class AmazonOrderCommitResponse(BaseModel):
    import_id: int
    filename: str
    marketplace: str
    row_count: int
    report_period_start: str | None
    report_period_end: str | None
    source_sha256: str | None


class AmazonOrderImportRow(BaseModel):
    import_id: int
    filename: str
    marketplace: str
    row_count: int
    report_period_start: str | None
    report_period_end: str | None
    fba_quantity: float
    fbm_quantity: float
    created_at: str


class AmazonOrderImportListResponse(BaseModel):
    rows: list[AmazonOrderImportRow]


def missing_connector_settings() -> list[str]:
    required = {
        "AMAZON_SP_API_REFRESH_TOKEN": settings.AMAZON_SP_API_REFRESH_TOKEN,
        "AMAZON_SP_API_LWA_CLIENT_ID": settings.AMAZON_SP_API_LWA_CLIENT_ID,
        "AMAZON_SP_API_LWA_CLIENT_SECRET": settings.AMAZON_SP_API_LWA_CLIENT_SECRET,
        "AMAZON_SP_API_AWS_ACCESS_KEY": settings.AMAZON_SP_API_AWS_ACCESS_KEY,
        "AMAZON_SP_API_AWS_SECRET_KEY": settings.AMAZON_SP_API_AWS_SECRET_KEY,
        "AMAZON_SP_API_AWS_ROLE_ARN": settings.AMAZON_SP_API_AWS_ROLE_ARN,
    }
    return [key for key, value in required.items() if not value]


def build_preview_response(preview, marketplace: str) -> AmazonOrderPreviewResponse:
    return AmazonOrderPreviewResponse(
        filename=preview.filename,
        marketplace=marketplace,
        report_type=REPORT_TYPE_ALL_ORDERS_BY_ORDER_DATE,
        encoding=preview.encoding,
        delimiter=preview.delimiter,
        row_count=preview.row_count,
        can_commit=preview.can_commit,
        headers=preview.headers,
        mapping=preview.mapping,
        missing_fields=preview.missing_fields,
        unknown_headers=preview.unknown_headers,
        totals=preview.totals,
        validation_errors=preview.validation_errors,
        sample_rows=preview.sample_rows,
    )


@router.get("/status", response_model=AmazonConnectorStatusResponse)
async def amazon_connector_status() -> AmazonConnectorStatusResponse:
    missing = missing_connector_settings()
    return AmazonConnectorStatusResponse(
        configured=not missing,
        missing_settings=missing,
        endpoint=settings.AMAZON_SP_API_ENDPOINT,
        region=settings.AMAZON_SP_API_REGION,
        phase_1_report_type=REPORT_TYPE_ALL_ORDERS_BY_ORDER_DATE,
    )


@router.post("/orders/preview", response_model=AmazonOrderPreviewResponse)
async def preview_amazon_orders_report(
    file: Annotated[UploadFile, File()],
    marketplace: Annotated[str, Form()],
    sample_size: Annotated[int, Form(ge=1, le=50)] = 10,
) -> AmazonOrderPreviewResponse:
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")
    preview = build_order_report_preview(
        filename=file.filename or "amazon-orders-report.tsv",
        content=content,
        marketplace=marketplace.upper(),
        sample_size=sample_size,
    )
    return build_preview_response(preview, marketplace.upper())


@router.post("/orders/commit", response_model=AmazonOrderCommitResponse)
async def commit_amazon_orders_report(
    file: Annotated[UploadFile, File()],
    marketplace: Annotated[str, Form()],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> AmazonOrderCommitResponse:
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")
    preview = build_order_report_preview(
        filename=file.filename or "amazon-orders-report.tsv",
        content=content,
        marketplace=marketplace.upper(),
    )
    if not preview.can_commit:
        raise HTTPException(
            status_code=400,
            detail={
                "missing_fields": preview.missing_fields,
                "validation_errors": preview.validation_errors,
            },
        )
    try:
        order_import = await commit_order_report_import(
            db=db,
            marketplace=marketplace.upper(),
            content=content,
            preview=preview,
        )
    except DuplicateImportError as exc:
        raise HTTPException(status_code=409, detail={"duplicate_import_id": exc.import_id}) from exc

    return AmazonOrderCommitResponse(
        import_id=order_import.id,
        filename=order_import.source_filename,
        marketplace=order_import.marketplace,
        row_count=order_import.row_count,
        report_period_start=order_import.report_period_start.isoformat() if order_import.report_period_start else None,
        report_period_end=order_import.report_period_end.isoformat() if order_import.report_period_end else None,
        source_sha256=order_import.source_sha256,
    )


@router.get("/orders/imports", response_model=AmazonOrderImportListResponse)
async def list_amazon_order_imports(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> AmazonOrderImportListResponse:
    result = await db.execute(
        select(
            AmazonOrderImport,
            func.coalesce(func.sum(AmazonOrderItem.quantity).filter(AmazonOrderItem.fulfillment_channel == "FBA"), 0).label("fba_quantity"),
            func.coalesce(func.sum(AmazonOrderItem.quantity).filter(AmazonOrderItem.fulfillment_channel == "FBM"), 0).label("fbm_quantity"),
        )
        .outerjoin(AmazonOrderItem, AmazonOrderItem.import_id == AmazonOrderImport.id)
        .group_by(AmazonOrderImport.id)
        .order_by(AmazonOrderImport.created_at.desc(), AmazonOrderImport.id.desc())
    )
    return AmazonOrderImportListResponse(
        rows=[
            AmazonOrderImportRow(
                import_id=row.AmazonOrderImport.id,
                filename=row.AmazonOrderImport.source_filename,
                marketplace=row.AmazonOrderImport.marketplace,
                row_count=row.AmazonOrderImport.row_count,
                report_period_start=row.AmazonOrderImport.report_period_start.isoformat() if row.AmazonOrderImport.report_period_start else None,
                report_period_end=row.AmazonOrderImport.report_period_end.isoformat() if row.AmazonOrderImport.report_period_end else None,
                fba_quantity=float(row.fba_quantity or 0),
                fbm_quantity=float(row.fbm_quantity or 0),
                created_at=row.AmazonOrderImport.created_at.isoformat(),
            )
            for row in result
        ]
    )


@router.post("/orders/sync")
async def sync_amazon_orders_report() -> dict:
    missing = missing_connector_settings()
    if missing:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Amazon SP-API connector is not configured yet.",
                "missing_settings": missing,
            },
        )
    raise HTTPException(
        status_code=501,
        detail="SP-API download worker is not enabled yet. Manual All Orders report import is available.",
    )
