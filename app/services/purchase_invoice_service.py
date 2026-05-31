from datetime import datetime
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ingestion.purchase_invoices import PurchaseInvoicePreview, calculate_sha256
from app.models.product_cost import ProductCost
from app.models.product_cost_import import ProductCostImport
from app.models.purchase_invoice import PurchaseInvoice
from app.models.purchase_invoice_line import PurchaseInvoiceLine
from app.services.amazon_payment_import_service import DuplicateImportError


async def commit_purchase_invoice(
    db: AsyncSession,
    content: bytes,
    preview: PurchaseInvoicePreview,
) -> PurchaseInvoice:
    source_sha256 = calculate_sha256(content)
    existing = await db.scalar(
        select(PurchaseInvoice).where(PurchaseInvoice.source_sha256 == source_sha256)
    )
    if existing:
        raise DuplicateImportError(existing.id)

    effective_date = preview.invoice_date or datetime.utcnow().date()

    invoice = PurchaseInvoice(
        source_filename=preview.filename,
        source_sha256=source_sha256,
        supplier_name=preview.supplier_name,
        invoice_number=preview.invoice_number,
        invoice_date=preview.invoice_date,
        due_date=preview.due_date,
        currency=preview.currency,
        subtotal_amount=Decimal(str(preview.totals["subtotal_amount"])),
        vat_amount=Decimal(str(preview.totals["vat_amount"])),
        total_amount=Decimal(str(preview.totals["total_amount"])),
        header_mapping=preview.mapping,
        row_count=len(preview.parsed_rows),
    )
    db.add(invoice)
    await db.flush()

    cost_import = ProductCostImport(
        source_filename=f"invoice_costs_{preview.filename}",
        source_sha256=source_sha256,
        currency=preview.currency,
        effective_date=effective_date,
        header_mapping={
            "product_name": "invoice.product_name",
            "sku": "invoice.sku_or_supplier_sku_or_ean",
            "purchase_cost": "invoice.unit_cost",
        },
        row_count=len(preview.parsed_rows),
    )
    db.add(cost_import)
    await db.flush()

    for row_number, (raw_row, parsed) in enumerate(zip(preview.raw_rows, preview.parsed_rows), start=2):
        sku = str(parsed["sku"] or parsed["supplier_sku"] or parsed["ean"] or "")
        db.add(
            PurchaseInvoiceLine(
                invoice_id=invoice.id,
                row_number=row_number,
                supplier_sku=parsed["supplier_sku"],
                sku=parsed["sku"],
                ean=parsed["ean"],
                product_name=str(parsed["product_name"]),
                quantity=parsed["quantity"],
                unit_cost=parsed["unit_cost"],
                line_net_amount=parsed["line_net_amount"],
                vat_rate_percent=parsed["vat_rate_percent"],
                vat_amount=parsed["vat_amount"],
                line_gross_amount=parsed["line_gross_amount"],
                currency=str(parsed["currency"]),
                raw_row=raw_row,
            )
        )
        if sku:
            db.add(
                ProductCost(
                    import_id=cost_import.id,
                    sku=sku,
                    product_name=str(parsed["product_name"]),
                    purchase_cost=parsed["unit_cost"],
                    currency=str(parsed["currency"]),
                    effective_date=effective_date,
                    raw_row={
                        "source": "purchase_invoice",
                        "invoice_id": invoice.id,
                        "invoice_number": preview.invoice_number,
                        "supplier_name": preview.supplier_name,
                        "raw_row": raw_row,
                    },
                )
            )

    await db.commit()
    await db.refresh(invoice)
    return invoice
