from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from pydantic import BaseModel, Field
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
from app.models.amazon_return_import import AmazonReturnImport
from app.models.amazon_return_item import AmazonReturnItem
from app.services.amazon_order_import_service import commit_order_report_import
from app.services.amazon_finances_sync_service import (
    AmazonFinancesSyncConflict,
    sync_finance_transactions,
)
from app.services.amazon_order_sync_service import sync_orders_report
from app.services.amazon_return_sync_service import sync_returns_report
from app.services.fba_inventory_sync_service import sync_fba_inventory
from app.services.amazon_reimbursement_sync_service import sync_reimbursements
from app.services.fba_storage_fee_sync_service import sync_storage_fees
from app.services.amazon_payment_import_service import DuplicateImportError
from app.services.amazon_sp_api_client import (
    DEFAULT_REPORTS_API_MIN_INTERVALS,
    EU_MARKETPLACES,
    MARKETPLACE_IDS,
    AmazonSpApiConfigError,
    AmazonSpApiError,
    missing_connector_settings,
)


router = APIRouter(prefix="/integrations/amazon-sp-api", tags=["amazon-sp-api"])


class AmazonConnectorStatusResponse(BaseModel):
    configured: bool
    missing_settings: list[str]
    endpoint: str
    region: str
    phase_1_report_type: str
    marketplace_ids: dict[str, str]
    eu_marketplaces: list[str]
    rate_limit_min_intervals_seconds: dict[str, float]


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


class AmazonOrderSyncRequest(BaseModel):
    marketplace: str = Field(min_length=2, max_length=3)
    start_date: date
    end_date: date
    poll_interval_seconds: int = Field(default=30, ge=10, le=300)
    wait_timeout_seconds: int = Field(default=300, ge=30, le=1800)


class AmazonPaymentSyncRequest(BaseModel):
    marketplace: str = Field(min_length=2, max_length=2)
    start_date: date
    end_date: date


class AmazonPaymentSyncResponse(BaseModel):
    status: str
    import_id: int | None
    marketplace: str
    transactions_received: int
    rows_imported: int
    rows_updated: int
    rows_skipped: int
    period_start: str
    period_end: str


class AmazonOrderSyncResponse(BaseModel):
    status: str
    report_id: str
    report_document_id: str | None
    import_id: int | None
    report_ids: list[str]
    report_document_ids: list[str]
    import_ids: list[int]
    filename: str | None
    row_count: int
    fba_quantity: float
    fbm_quantity: float
    processing_status: str


class AmazonReturnImportRow(BaseModel):
    import_id: int
    filename: str
    marketplace: str
    row_count: int
    report_period_start: str | None
    report_period_end: str | None
    created_at: str


class AmazonReturnImportListResponse(BaseModel):
    rows: list[AmazonReturnImportRow]


class AmazonReturnSyncResponse(BaseModel):
    status: str
    report_id: str
    report_document_id: str
    import_id: int
    filename: str
    row_count: int
    processing_status: str


class FbaInventorySyncResponse(BaseModel):
    report_id: str
    report_document_id: str
    captured_at: str
    rows: int
    fulfillable_quantity: float
    reserved_quantity: float
    inbound_quantity: float
    processing_status: str


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
        marketplace_ids=MARKETPLACE_IDS,
        eu_marketplaces=list(EU_MARKETPLACES),
        rate_limit_min_intervals_seconds=DEFAULT_REPORTS_API_MIN_INTERVALS,
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


@router.post("/orders/sync", response_model=AmazonOrderSyncResponse)
async def sync_amazon_orders_report(
    payload: AmazonOrderSyncRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> AmazonOrderSyncResponse:
    missing = missing_connector_settings()
    if missing:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Amazon SP-API connector is not configured yet.",
                "missing_settings": missing,
            },
        )
    if payload.end_date < payload.start_date:
        raise HTTPException(status_code=400, detail="end_date must be greater than or equal to start_date.")
    try:
        result = await sync_orders_report(
            db=db,
            marketplace=payload.marketplace.upper(),
            start_date=payload.start_date,
            end_date=payload.end_date,
            poll_interval_seconds=payload.poll_interval_seconds,
            wait_timeout_seconds=payload.wait_timeout_seconds,
        )
    except AmazonSpApiConfigError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except AmazonSpApiError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    return AmazonOrderSyncResponse(
        status=result.status,
        report_id=result.report_id or "",
        report_document_id=result.report_document_id,
        import_id=result.import_id,
        report_ids=result.report_ids,
        report_document_ids=result.report_document_ids,
        import_ids=result.import_ids,
        filename=result.filename,
        row_count=result.row_count,
        fba_quantity=result.fba_quantity,
        fbm_quantity=result.fbm_quantity,
        processing_status=result.processing_status,
    )


@router.post("/payments/sync", response_model=AmazonPaymentSyncResponse)
async def sync_amazon_payments(
    payload: AmazonPaymentSyncRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> AmazonPaymentSyncResponse:
    if payload.end_date < payload.start_date:
        raise HTTPException(
            status_code=400,
            detail="end_date must be greater than or equal to start_date.",
        )
    if (payload.end_date - payload.start_date).days > 180:
        raise HTTPException(
            status_code=400,
            detail="Payments sync period cannot exceed 181 days.",
        )
    try:
        result = await sync_finance_transactions(
            db=db,
            marketplace=payload.marketplace,
            start_date=payload.start_date,
            end_date=payload.end_date,
        )
    except AmazonSpApiConfigError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except AmazonFinancesSyncConflict as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except AmazonSpApiError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    return AmazonPaymentSyncResponse(**result.__dict__)


@router.get("/returns/imports", response_model=AmazonReturnImportListResponse)
async def list_amazon_return_imports(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> AmazonReturnImportListResponse:
    imports = list(
        await db.scalars(
            select(AmazonReturnImport).order_by(
                AmazonReturnImport.created_at.desc(),
                AmazonReturnImport.id.desc(),
            )
        )
    )
    return AmazonReturnImportListResponse(
        rows=[
            AmazonReturnImportRow(
                import_id=row.id,
                filename=row.source_filename,
                marketplace=row.marketplace,
                row_count=row.row_count,
                report_period_start=row.report_period_start.isoformat() if row.report_period_start else None,
                report_period_end=row.report_period_end.isoformat() if row.report_period_end else None,
                created_at=row.created_at.isoformat(),
            )
            for row in imports
        ]
    )


@router.post("/returns/sync", response_model=AmazonReturnSyncResponse)
async def sync_amazon_returns_report(
    payload: AmazonOrderSyncRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> AmazonReturnSyncResponse:
    if payload.end_date < payload.start_date:
        raise HTTPException(status_code=400, detail="end_date must be greater than or equal to start_date.")
    try:
        result = await sync_returns_report(
            db=db,
            marketplace=payload.marketplace.upper(),
            start_date=payload.start_date,
            end_date=payload.end_date,
            poll_interval_seconds=payload.poll_interval_seconds,
            wait_timeout_seconds=payload.wait_timeout_seconds,
        )
    except AmazonSpApiConfigError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except AmazonSpApiError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    return AmazonReturnSyncResponse(**result.__dict__)


@router.post("/inventory/sync", response_model=FbaInventorySyncResponse)
async def sync_amazon_fba_inventory(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> FbaInventorySyncResponse:
    try:
        result = await sync_fba_inventory(db=db)
    except AmazonSpApiConfigError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except AmazonSpApiError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    return FbaInventorySyncResponse(**result.__dict__)


@router.post("/reimbursements/sync")
async def sync_amazon_reimbursements(
    payload: AmazonOrderSyncRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> dict:
    if payload.end_date < payload.start_date:
        raise HTTPException(status_code=400, detail="end_date must be greater than or equal to start_date.")
    try:
        return await sync_reimbursements(db, payload.start_date, payload.end_date)
    except AmazonSpApiConfigError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except AmazonSpApiError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@router.post("/storage-fees/sync")
async def sync_amazon_storage_fees(
    payload: AmazonOrderSyncRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> dict:
    try:
        return await sync_storage_fees(db, payload.start_date)
    except AmazonSpApiConfigError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except AmazonSpApiError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
