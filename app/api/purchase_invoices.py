from datetime import date
from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile
from pydantic import BaseModel, Field
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.ingestion.purchase_invoices import build_purchase_invoice_preview, serialize_row
from app.models.purchase_invoice import PurchaseInvoice
from app.models.purchase_invoice_line import PurchaseInvoiceLine
from app.models.product_cost import ProductCost
from app.models.product_cost_import import ProductCostImport
from app.models.product_mapping import ProductMapping
from app.services.amazon_payment_import_service import DuplicateImportError
from app.services.purchase_invoice_service import commit_purchase_invoice
from app.services.supplier_catalog_service import enrich_invoice_rows_from_catalog


router = APIRouter(prefix="/imports/purchase-invoices", tags=["purchase-invoices"])

VAT_INCLUDED = "vat_included"
NO_VAT = "no_vat"
VAT_UNKNOWN = "vat_unknown"


def decimal_or_zero(value) -> Decimal:
    if value is None:
        return Decimal("0")
    if isinstance(value, Decimal):
        return value
    return Decimal(str(value))


def preview_vat_status(preview) -> str:
    rows = preview.parsed_rows or []
    has_vat_signal = bool(
        {"vat_rate_percent", "vat_amount", "line_gross_amount"} & set(preview.mapping)
    ) or any(
        row.get("vat_rate_percent") is not None
        or row.get("vat_amount") is not None
        or row.get("line_gross_amount") is not None
        for row in rows
    )
    vat_amount = decimal_or_zero(preview.totals.get("vat_amount"))
    if vat_amount > 0:
        return VAT_INCLUDED
    if has_vat_signal:
        return NO_VAT
    return VAT_UNKNOWN


def invoice_vat_status(invoice: PurchaseInvoice) -> str:
    vat_amount = decimal_or_zero(invoice.vat_amount)
    if vat_amount > 0:
        return VAT_INCLUDED
    has_vat_signal = bool(
        {"vat_rate_percent", "vat_amount", "line_gross_amount"} & set(invoice.header_mapping or {})
    )
    if has_vat_signal:
        return NO_VAT
    return VAT_UNKNOWN


def line_vat_status(line: PurchaseInvoiceLine) -> str:
    vat_rate = decimal_or_zero(line.vat_rate_percent)
    vat_amount = decimal_or_zero(line.vat_amount)
    if vat_rate > 0 or vat_amount > 0:
        return VAT_INCLUDED
    if line.vat_rate_percent is not None or line.vat_amount is not None or line.line_gross_amount is not None:
        return NO_VAT
    return VAT_UNKNOWN


class PurchaseInvoicePreviewResponse(BaseModel):
    filename: str
    supplier_name: str
    invoice_number: str | None
    invoice_date: str | None
    due_date: str | None
    currency: str
    vat_status: str
    row_count: int
    parsed_row_count: int
    can_commit: bool
    headers: list[str]
    mapping: dict[str, str]
    missing_fields: list[str]
    ambiguous_headers: dict[str, list[str]]
    unknown_headers: list[str]
    validation_errors: list[str]
    totals: dict[str, float]
    sample_rows: list[dict[str, str]]
    normalized_sample_rows: list[dict[str, str | float | None]]


class PurchaseInvoiceCommitResponse(BaseModel):
    invoice_id: int
    filename: str
    supplier_name: str
    invoice_number: str | None
    invoice_date: str | None
    currency: str
    row_count: int
    total_amount: float | None
    source_sha256: str | None


class PurchaseInvoiceRow(BaseModel):
    invoice_id: int
    filename: str
    supplier_name: str
    invoice_number: str | None
    invoice_date: str | None
    currency: str
    row_count: int
    subtotal_amount: float | None
    vat_amount: float | None
    total_amount: float | None
    vat_status: str
    created_at: str


class PurchaseInvoiceLineRow(BaseModel):
    id: int
    invoice_id: int
    sku: str | None
    supplier_sku: str | None
    ean: str | None
    line_type: str
    expense_category: str | None
    product_name: str
    quantity: float
    unit_cost: float
    line_net_amount: float | None
    vat_rate_percent: float | None
    vat_amount: float | None
    line_gross_amount: float | None
    vat_status: str
    currency: str


class PurchaseInvoiceListResponse(BaseModel):
    rows: list[PurchaseInvoiceRow]


class PurchaseInvoiceLinesResponse(BaseModel):
    rows: list[PurchaseInvoiceLineRow]


class PurchaseInvoiceLineUpdateRequest(BaseModel):
    supplier_sku: str | None = Field(default=None, max_length=120)
    sku: str | None = Field(default=None, max_length=120)
    ean: str | None = Field(default=None, max_length=64)
    product_name: str = Field(min_length=1)


class DeleteInvoiceResponse(BaseModel):
    invoice_id: int
    deleted: bool


def preview_response(preview) -> PurchaseInvoicePreviewResponse:
    return PurchaseInvoicePreviewResponse(
        filename=preview.filename,
        supplier_name=preview.supplier_name,
        invoice_number=preview.invoice_number,
        invoice_date=preview.invoice_date.isoformat() if preview.invoice_date else None,
        due_date=preview.due_date.isoformat() if preview.due_date else None,
        currency=preview.currency,
        vat_status=preview_vat_status(preview),
        row_count=preview.row_count,
        parsed_row_count=len(preview.parsed_rows),
        can_commit=preview.can_commit,
        headers=preview.headers,
        mapping=preview.mapping,
        missing_fields=preview.missing_fields,
        ambiguous_headers=preview.ambiguous_headers,
        unknown_headers=preview.unknown_headers,
        validation_errors=preview.validation_errors,
        totals=preview.totals,
        sample_rows=preview.sample_rows,
        normalized_sample_rows=preview.normalized_sample_rows,
    )


async def enrich_preview_from_catalog(db: AsyncSession, preview) -> None:
    enriched_count = await enrich_invoice_rows_from_catalog(
        db=db,
        supplier_name=preview.supplier_name,
        parsed_rows=preview.parsed_rows,
    )
    if enriched_count:
        sample_size = len(preview.normalized_sample_rows) or 10
        preview.normalized_sample_rows[:] = [
            serialize_row(row) for row in preview.parsed_rows[:sample_size]
        ]


@router.post("/preview", response_model=PurchaseInvoicePreviewResponse)
async def preview_purchase_invoice(
    file: Annotated[UploadFile, File()],
    db: Annotated[AsyncSession, Depends(get_db)],
    supplier_name: Annotated[str, Form()] = "",
    invoice_number: Annotated[str | None, Form()] = None,
    invoice_date: Annotated[date | None, Form()] = None,
    due_date: Annotated[date | None, Form()] = None,
    currency: Annotated[str, Form(min_length=3, max_length=8)] = "EUR",
    sample_size: Annotated[int, Form(ge=1, le=50)] = 10,
) -> PurchaseInvoicePreviewResponse:
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")
    try:
        preview = build_purchase_invoice_preview(
            filename=file.filename or "purchase-invoice",
            content=content,
            supplier_name=supplier_name,
            invoice_number=invoice_number,
            invoice_date=invoice_date,
            due_date=due_date,
            currency=currency,
            sample_size=sample_size,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    await enrich_preview_from_catalog(db, preview)
    return preview_response(preview)


@router.post("/commit", response_model=PurchaseInvoiceCommitResponse)
async def commit_purchase_invoice_endpoint(
    file: Annotated[UploadFile, File()],
    db: Annotated[AsyncSession, Depends(get_db)],
    supplier_name: Annotated[str, Form()] = "",
    invoice_number: Annotated[str | None, Form()] = None,
    invoice_date: Annotated[date | None, Form()] = None,
    due_date: Annotated[date | None, Form()] = None,
    currency: Annotated[str, Form(min_length=3, max_length=8)] = "EUR",
) -> PurchaseInvoiceCommitResponse:
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")
    try:
        preview = build_purchase_invoice_preview(
            filename=file.filename or "purchase-invoice",
            content=content,
            supplier_name=supplier_name,
            invoice_number=invoice_number,
            invoice_date=invoice_date,
            due_date=due_date,
            currency=currency,
            sample_size=10,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    await enrich_preview_from_catalog(db, preview)
    if not preview.can_commit:
        raise HTTPException(status_code=400, detail=preview_response(preview).model_dump())
    try:
        invoice = await commit_purchase_invoice(db=db, content=content, preview=preview)
    except DuplicateImportError as exc:
        raise HTTPException(
            status_code=409,
            detail={"message": "File was already imported.", "invoice_id": exc.import_id},
        ) from exc
    return PurchaseInvoiceCommitResponse(
        invoice_id=invoice.id,
        filename=invoice.source_filename,
        supplier_name=invoice.supplier_name,
        invoice_number=invoice.invoice_number,
        invoice_date=invoice.invoice_date.isoformat() if invoice.invoice_date else None,
        currency=invoice.currency,
        row_count=invoice.row_count,
        total_amount=float(invoice.total_amount) if invoice.total_amount is not None else None,
        source_sha256=invoice.source_sha256,
    )


@router.get("", response_model=PurchaseInvoiceListResponse)
async def list_purchase_invoices(
    db: Annotated[AsyncSession, Depends(get_db)],
    start_date: Annotated[date | None, Query()] = None,
    end_date: Annotated[date | None, Query()] = None,
) -> PurchaseInvoiceListResponse:
    statement = select(PurchaseInvoice)
    if start_date:
        statement = statement.where(PurchaseInvoice.invoice_date >= start_date)
    if end_date:
        statement = statement.where(PurchaseInvoice.invoice_date <= end_date)
    result = await db.scalars(statement.order_by(PurchaseInvoice.created_at.desc()))
    return PurchaseInvoiceListResponse(
        rows=[
            PurchaseInvoiceRow(
                invoice_id=row.id,
                filename=row.source_filename,
                supplier_name=row.supplier_name,
                invoice_number=row.invoice_number,
                invoice_date=row.invoice_date.isoformat() if row.invoice_date else None,
                currency=row.currency,
                row_count=row.row_count,
                subtotal_amount=float(row.subtotal_amount) if row.subtotal_amount is not None else None,
                vat_amount=float(row.vat_amount) if row.vat_amount is not None else None,
                total_amount=float(row.total_amount) if row.total_amount is not None else None,
                vat_status=invoice_vat_status(row),
                created_at=row.created_at.isoformat(),
            )
            for row in result
        ]
    )


@router.get("/{invoice_id}/lines", response_model=PurchaseInvoiceLinesResponse)
async def list_purchase_invoice_lines(
    invoice_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> PurchaseInvoiceLinesResponse:
    result = await db.scalars(
        select(PurchaseInvoiceLine)
        .where(PurchaseInvoiceLine.invoice_id == invoice_id)
        .order_by(PurchaseInvoiceLine.row_number)
    )
    return PurchaseInvoiceLinesResponse(
        rows=[
            PurchaseInvoiceLineRow(
                id=row.id,
                invoice_id=row.invoice_id,
                sku=row.sku,
                supplier_sku=row.supplier_sku,
                ean=row.ean,
                line_type=row.line_type,
                expense_category=row.expense_category,
                product_name=row.product_name,
                quantity=float(row.quantity),
                unit_cost=float(row.unit_cost),
                line_net_amount=float(row.line_net_amount) if row.line_net_amount is not None else None,
                vat_rate_percent=float(row.vat_rate_percent) if row.vat_rate_percent is not None else None,
                vat_amount=float(row.vat_amount) if row.vat_amount is not None else None,
                line_gross_amount=float(row.line_gross_amount) if row.line_gross_amount is not None else None,
                vat_status=line_vat_status(row),
                currency=row.currency,
            )
            for row in result
        ]
    )


@router.put("/lines/{line_id}", response_model=PurchaseInvoiceLineRow)
async def update_purchase_invoice_line(
    line_id: int,
    payload: PurchaseInvoiceLineUpdateRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> PurchaseInvoiceLineRow:
    line = await db.get(PurchaseInvoiceLine, line_id)
    if line is None:
        raise HTTPException(status_code=404, detail="Purchase invoice line was not found.")

    product_name = payload.product_name.strip()
    if not product_name:
        raise HTTPException(status_code=400, detail="Product name is required.")

    old_sku = line.sku or line.supplier_sku or line.ean
    line.supplier_sku = (payload.supplier_sku or "").strip() or None
    line.sku = (payload.sku or "").strip() or None
    line.ean = (payload.ean or "").strip() or None
    line.product_name = product_name
    new_sku = line.sku or line.supplier_sku or line.ean

    raw_row = dict(line.raw_row or {})
    raw_row["operator_corrected"] = True
    raw_row["operator_product_name"] = product_name
    raw_row["operator_sku"] = line.sku
    raw_row["operator_supplier_sku"] = line.supplier_sku
    raw_row["operator_ean"] = line.ean
    line.raw_row = raw_row

    mappings = await db.scalars(
        select(ProductMapping).where(ProductMapping.invoice_line_id == line.id)
    )
    for mapping in mappings:
        mapping.supplier_sku = line.supplier_sku
        mapping.sku = line.sku
        mapping.ean = line.ean
        mapping.invoice_product_name = line.product_name

    invoice = await db.get(PurchaseInvoice, line.invoice_id)
    if invoice and invoice.source_sha256:
        cost_import = await db.scalar(
            select(ProductCostImport)
            .where(ProductCostImport.source_sha256 == invoice.source_sha256)
            .where(ProductCostImport.source_filename.ilike("invoice_costs_%"))
        )
        if cost_import:
            costs = await db.scalars(
                select(ProductCost)
                .where(ProductCost.import_id == cost_import.id)
                .where(ProductCost.raw_row["invoice_id"].as_integer() == line.invoice_id)
                .where(ProductCost.sku == old_sku)
            )
            for cost in costs:
                cost.sku = new_sku or cost.sku
                cost.product_name = line.product_name
                cost.raw_row = {
                    **(cost.raw_row or {}),
                    "ean": line.ean,
                    "operator_corrected": True,
                    "operator_product_name": line.product_name,
                    "operator_sku": line.sku,
                    "operator_supplier_sku": line.supplier_sku,
                }

    await db.commit()
    await db.refresh(line)
    return PurchaseInvoiceLineRow(
        id=line.id,
        invoice_id=line.invoice_id,
        sku=line.sku,
        supplier_sku=line.supplier_sku,
        ean=line.ean,
        line_type=line.line_type,
        expense_category=line.expense_category,
        product_name=line.product_name,
        quantity=float(line.quantity),
        unit_cost=float(line.unit_cost),
        line_net_amount=float(line.line_net_amount) if line.line_net_amount is not None else None,
        vat_rate_percent=float(line.vat_rate_percent) if line.vat_rate_percent is not None else None,
        vat_amount=float(line.vat_amount) if line.vat_amount is not None else None,
        line_gross_amount=float(line.line_gross_amount) if line.line_gross_amount is not None else None,
        vat_status=line_vat_status(line),
        currency=line.currency,
    )


@router.delete("/{invoice_id}", response_model=DeleteInvoiceResponse)
async def delete_purchase_invoice(
    invoice_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> DeleteInvoiceResponse:
    invoice = await db.get(PurchaseInvoice, invoice_id)
    if invoice is None:
        raise HTTPException(status_code=404, detail="Purchase invoice not found.")

    line_ids = await db.scalars(
        select(PurchaseInvoiceLine.id).where(PurchaseInvoiceLine.invoice_id == invoice_id)
    )
    invoice_line_ids = list(line_ids)
    if invoice_line_ids:
        await db.execute(
            delete(ProductMapping).where(ProductMapping.invoice_line_id.in_(invoice_line_ids))
        )

    cost_import = await db.scalar(
        select(ProductCostImport)
        .where(ProductCostImport.source_sha256 == invoice.source_sha256)
        .where(ProductCostImport.source_filename.ilike("invoice_costs_%"))
    )
    if cost_import:
        await db.execute(delete(ProductCost).where(ProductCost.import_id == cost_import.id))
        await db.delete(cost_import)

    await db.execute(
        delete(PurchaseInvoiceLine).where(PurchaseInvoiceLine.invoice_id == invoice_id)
    )
    await db.delete(invoice)
    await db.commit()

    return DeleteInvoiceResponse(invoice_id=invoice_id, deleted=True)
