from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from pydantic import BaseModel
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.ingestion.amazon_reports.payment_transactions import (
    build_payment_transaction_preview,
)
from app.services.amazon_payment_import_service import (
    DuplicateImportError,
    commit_payment_transaction_import,
)
from app.models.amazon_payment_import import AmazonPaymentImport
from app.models.amazon_payment_transaction import AmazonPaymentTransaction
from app.models.amazon_payment_transaction_raw import AmazonPaymentTransactionRaw


router = APIRouter(prefix="/imports/amazon-payments", tags=["amazon-payments"])


class AmazonPaymentPreviewResponse(BaseModel):
    filename: str
    marketplace: str | None
    report_type: str
    encoding: str
    delimiter: str
    row_count: int
    currency: str | None
    can_commit: bool
    headers: list[str]
    mapping: dict[str, str]
    missing_fields: list[str]
    ambiguous_headers: dict[str, list[str]]
    unknown_headers: list[str]
    validation_errors: list[str]
    totals_by_transaction_type: dict[str, dict[str, int | float]]
    sample_rows: list[dict[str, str]]
    normalized_sample_rows: list[dict[str, str | int | float | None]]


class AmazonPaymentCommitResponse(BaseModel):
    import_id: int
    filename: str
    marketplace: str
    row_count: int
    currency: str | None
    report_period_start: str | None
    report_period_end: str | None
    source_sha256: str | None


class AmazonPaymentImportRow(BaseModel):
    import_id: int
    filename: str
    marketplace: str
    row_count: int
    report_period_start: str | None
    report_period_end: str | None
    created_at: str


class AmazonPaymentImportListResponse(BaseModel):
    rows: list[AmazonPaymentImportRow]


class DeleteImportResponse(BaseModel):
    import_id: int
    deleted: bool


def build_preview_response(
    preview,
    marketplace: str | None,
) -> AmazonPaymentPreviewResponse:
    return AmazonPaymentPreviewResponse(
        filename=preview.filename,
        marketplace=marketplace,
        report_type="amazon_payment_transactions",
        encoding=preview.encoding,
        delimiter=preview.delimiter,
        row_count=preview.row_count,
        currency=preview.currency,
        can_commit=preview.can_commit,
        headers=preview.headers,
        mapping=preview.mapping_result.mapping,
        missing_fields=preview.mapping_result.missing_fields,
        ambiguous_headers=preview.mapping_result.ambiguous_headers,
        unknown_headers=preview.mapping_result.unknown_headers,
        validation_errors=preview.validation_errors,
        totals_by_transaction_type=preview.totals_by_transaction_type,
        sample_rows=preview.sample_rows,
        normalized_sample_rows=preview.normalized_sample_rows,
    )


@router.post("/preview", response_model=AmazonPaymentPreviewResponse)
async def preview_amazon_payment_transactions(
    file: Annotated[UploadFile, File()],
    marketplace: Annotated[str | None, Form()] = None,
    sample_size: Annotated[int, Form(ge=1, le=50)] = 10,
) -> AmazonPaymentPreviewResponse:
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    preview = build_payment_transaction_preview(
        filename=file.filename or "upload.csv",
        content=content,
        sample_size=sample_size,
    )

    return build_preview_response(preview, marketplace)


@router.get("", response_model=AmazonPaymentImportListResponse)
async def list_amazon_payment_imports(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> AmazonPaymentImportListResponse:
    result = await db.scalars(
        select(AmazonPaymentImport).order_by(AmazonPaymentImport.created_at.desc())
    )
    return AmazonPaymentImportListResponse(
        rows=[
            AmazonPaymentImportRow(
                import_id=row.id,
                filename=row.source_filename,
                marketplace=row.marketplace,
                row_count=row.row_count,
                report_period_start=row.report_period_start.date().isoformat()
                if row.report_period_start
                else None,
                report_period_end=row.report_period_end.date().isoformat()
                if row.report_period_end
                else None,
                created_at=row.created_at.isoformat(),
            )
            for row in result
        ]
    )


@router.delete("/{import_id}", response_model=DeleteImportResponse)
async def delete_amazon_payment_import(
    import_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> DeleteImportResponse:
    payment_import = await db.get(AmazonPaymentImport, import_id)
    if payment_import is None:
        raise HTTPException(status_code=404, detail="Amazon payment import not found.")

    await db.execute(
        delete(AmazonPaymentTransaction).where(
            AmazonPaymentTransaction.import_id == import_id
        )
    )
    await db.execute(
        delete(AmazonPaymentTransactionRaw).where(
            AmazonPaymentTransactionRaw.import_id == import_id
        )
    )
    await db.delete(payment_import)
    await db.commit()

    return DeleteImportResponse(import_id=import_id, deleted=True)


@router.post("/commit", response_model=AmazonPaymentCommitResponse)
async def commit_amazon_payment_transactions(
    file: Annotated[UploadFile, File()],
    marketplace: Annotated[str, Form(min_length=2, max_length=16)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> AmazonPaymentCommitResponse:
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    preview = build_payment_transaction_preview(
        filename=file.filename or "upload.csv",
        content=content,
        sample_size=10,
    )
    if not preview.can_commit:
        raise HTTPException(
            status_code=400,
            detail=build_preview_response(preview, marketplace).model_dump(),
        )

    try:
        payment_import = await commit_payment_transaction_import(
            db=db,
            marketplace=marketplace.upper(),
            content=content,
            preview=preview,
        )
    except DuplicateImportError as exc:
        raise HTTPException(
            status_code=409,
            detail={"message": "File was already imported.", "import_id": exc.import_id},
        ) from exc

    return AmazonPaymentCommitResponse(
        import_id=payment_import.id,
        filename=payment_import.source_filename,
        marketplace=payment_import.marketplace,
        row_count=payment_import.row_count,
        currency=preview.currency,
        report_period_start=payment_import.report_period_start.date().isoformat()
        if payment_import.report_period_start
        else None,
        report_period_end=payment_import.report_period_end.date().isoformat()
        if payment_import.report_period_end
        else None,
        source_sha256=payment_import.source_sha256,
    )
