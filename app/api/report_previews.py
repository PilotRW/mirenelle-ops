from typing import Annotated, Literal

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.ingestion.generic_reports import build_generic_report_preview
from app.models.generic_report_import import GenericReportImport
from app.services.amazon_payment_import_service import DuplicateImportError
from app.services.generic_report_import_service import commit_generic_report_import


router = APIRouter(prefix="/imports/report-preview", tags=["report-preview"])


ReportType = Literal["customer_returns", "reimbursements", "service_fees"]


class GenericReportPreviewResponse(BaseModel):
    filename: str
    report_type: str
    encoding: str
    delimiter: str
    headers: list[str]
    row_count: int
    sample_rows: list[dict[str, str]]


class GenericReportCommitResponse(BaseModel):
    import_id: int
    report_type: str
    filename: str
    row_count: int
    source_sha256: str | None


class GenericReportImportRow(BaseModel):
    import_id: int
    report_type: str
    filename: str
    row_count: int
    created_at: str


class GenericReportImportListResponse(BaseModel):
    rows: list[GenericReportImportRow]


@router.post("", response_model=GenericReportPreviewResponse)
async def preview_generic_report(
    file: Annotated[UploadFile, File()],
    report_type: Annotated[ReportType, Form()],
    sample_size: Annotated[int, Form(ge=1, le=50)] = 10,
) -> GenericReportPreviewResponse:
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    preview = build_generic_report_preview(
        filename=file.filename or "report.csv",
        content=content,
        report_type=report_type,
        sample_size=sample_size,
    )
    return GenericReportPreviewResponse(
        filename=preview.filename,
        report_type=preview.report_type,
        encoding=preview.encoding,
        delimiter=preview.delimiter,
        headers=preview.headers,
        row_count=preview.row_count,
        sample_rows=preview.sample_rows,
    )


@router.get("", response_model=GenericReportImportListResponse)
async def list_generic_report_imports(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> GenericReportImportListResponse:
    result = await db.scalars(
        select(GenericReportImport).order_by(GenericReportImport.created_at.desc())
    )
    return GenericReportImportListResponse(
        rows=[
            GenericReportImportRow(
                import_id=row.id,
                report_type=row.report_type,
                filename=row.source_filename,
                row_count=row.row_count,
                created_at=row.created_at.isoformat(),
            )
            for row in result
        ]
    )


@router.post("/commit", response_model=GenericReportCommitResponse)
async def commit_generic_report(
    file: Annotated[UploadFile, File()],
    report_type: Annotated[ReportType, Form()],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> GenericReportCommitResponse:
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    preview = build_generic_report_preview(
        filename=file.filename or "report.csv",
        content=content,
        report_type=report_type,
        sample_size=10,
    )
    try:
        report_import = await commit_generic_report_import(
            db=db,
            content=content,
            preview=preview,
        )
    except DuplicateImportError as exc:
        raise HTTPException(
            status_code=409,
            detail={"message": "File was already imported.", "import_id": exc.import_id},
        ) from exc

    return GenericReportCommitResponse(
        import_id=report_import.id,
        report_type=report_import.report_type,
        filename=report_import.source_filename,
        row_count=report_import.row_count,
        source_sha256=report_import.source_sha256,
    )
