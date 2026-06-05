from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ingestion.purchase_invoices import PRODUCT_LINE_TYPE, PurchaseInvoicePreview, calculate_sha256
from app.models.product_cost import ProductCost
from app.models.product_cost_import import ProductCostImport
from app.models.purchase_invoice import PurchaseInvoice
from app.models.purchase_invoice_line import PurchaseInvoiceLine
from app.services.amazon_payment_import_service import DuplicateImportError
from app.services.app_settings import get_landed_cost_allocation_method


CENT = Decimal("0.01")
LANDED_ALLOCATION_LABELS = {
    "by_quantity": "invoice_inbound_shipping_by_quantity",
    "by_line_value": "invoice_inbound_shipping_by_line_value",
}


def money(value: Decimal | int | str | None) -> Decimal:
    if value is None:
        return Decimal("0")
    if isinstance(value, Decimal):
        return value
    return Decimal(str(value))


def allocated_landed_costs(parsed_rows: list[dict], allocation_method: str = "by_quantity") -> dict[int, dict[str, Decimal | str]]:
    product_indexes = [
        index
        for index, row in enumerate(parsed_rows)
        if row["line_type"] == PRODUCT_LINE_TYPE and (row["sku"] or row["supplier_sku"] or row["ean"])
    ]
    inbound_shipping_total = sum(
        (
            money(row.get("line_net_amount"))
            for row in parsed_rows
            if row.get("line_type") == "inbound_shipping"
        ),
        Decimal("0"),
    )
    if not product_indexes or inbound_shipping_total <= 0:
        return {
            index: {
                "base_unit_cost": money(parsed_rows[index].get("unit_cost")),
                "allocated_inbound_shipping": Decimal("0"),
                "allocated_inbound_shipping_per_unit": Decimal("0"),
                "landed_unit_cost": money(parsed_rows[index].get("unit_cost")).quantize(CENT, rounding=ROUND_HALF_UP),
                "landed_cost_allocation": LANDED_ALLOCATION_LABELS.get(allocation_method, LANDED_ALLOCATION_LABELS["by_quantity"]),
            }
            for index in product_indexes
        }

    if allocation_method == "by_line_value":
        allocation_basis = {
            index: money(parsed_rows[index].get("line_net_amount"))
            for index in product_indexes
        }
        fallback_basis = {
            index: money(parsed_rows[index].get("quantity"))
            for index in product_indexes
        }
    else:
        allocation_method = "by_quantity"
        allocation_basis = {
            index: money(parsed_rows[index].get("quantity"))
            for index in product_indexes
        }
        fallback_basis = {
            index: money(parsed_rows[index].get("line_net_amount"))
            for index in product_indexes
        }
    basis_total = sum(allocation_basis.values(), Decimal("0"))
    if basis_total <= 0:
        allocation_basis = fallback_basis
        basis_total = sum(allocation_basis.values(), Decimal("0"))

    allocations: dict[int, dict[str, Decimal]] = {}
    allocated_so_far = Decimal("0")
    for position, index in enumerate(product_indexes):
        row = parsed_rows[index]
        quantity = money(row.get("quantity"))
        base_unit_cost = money(row.get("unit_cost"))
        if basis_total <= 0:
            allocated = Decimal("0")
        elif position == len(product_indexes) - 1:
            allocated = inbound_shipping_total - allocated_so_far
        else:
            allocated = (inbound_shipping_total * allocation_basis[index] / basis_total).quantize(CENT, rounding=ROUND_HALF_UP)
            allocated_so_far += allocated
        allocated_per_unit = (
            (allocated / quantity).quantize(CENT, rounding=ROUND_HALF_UP)
            if quantity > 0
            else Decimal("0")
        )
        allocations[index] = {
            "base_unit_cost": base_unit_cost,
            "allocated_inbound_shipping": allocated,
            "allocated_inbound_shipping_per_unit": allocated_per_unit,
            "landed_unit_cost": (base_unit_cost + allocated_per_unit).quantize(CENT, rounding=ROUND_HALF_UP),
            "landed_cost_allocation": LANDED_ALLOCATION_LABELS[allocation_method],
        }
    return allocations


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

    product_rows = [
        parsed
        for parsed in preview.parsed_rows
        if parsed["line_type"] == PRODUCT_LINE_TYPE and (parsed["sku"] or parsed["supplier_sku"] or parsed["ean"])
    ]
    allocation_method = await get_landed_cost_allocation_method(db)

    cost_import = ProductCostImport(
        source_filename=f"invoice_costs_{preview.filename}",
        source_sha256=source_sha256,
        currency=preview.currency,
        effective_date=effective_date,
        header_mapping={
            "product_name": "invoice.product_name",
            "sku": "invoice.sku_or_supplier_sku_or_ean",
            "purchase_cost": "invoice.unit_cost + allocated_inbound_shipping_per_unit",
            "landed_cost_allocation_method": allocation_method,
        },
        row_count=len(product_rows),
    )
    db.add(cost_import)
    await db.flush()

    landed_costs = allocated_landed_costs(preview.parsed_rows, allocation_method=allocation_method)

    for row_number, (raw_row, parsed) in enumerate(zip(preview.raw_rows, preview.parsed_rows), start=2):
        sku = str(parsed["sku"] or parsed["supplier_sku"] or parsed["ean"] or "")
        db.add(
            PurchaseInvoiceLine(
                invoice_id=invoice.id,
                row_number=row_number,
                supplier_sku=parsed["supplier_sku"],
                sku=parsed["sku"],
                ean=parsed["ean"],
                line_type=str(parsed["line_type"]),
                expense_category=parsed["expense_category"],
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
        if sku and parsed["line_type"] == PRODUCT_LINE_TYPE:
            landed = landed_costs.get(row_number - 2, {})
            db.add(
                ProductCost(
                    import_id=cost_import.id,
                    sku=sku,
                    product_name=str(parsed["product_name"]),
                    purchase_cost=landed.get("landed_unit_cost", parsed["unit_cost"]),
                    currency=str(parsed["currency"]),
                    effective_date=effective_date,
                    raw_row={
                        "source": "purchase_invoice",
                        "invoice_id": invoice.id,
                        "invoice_number": preview.invoice_number,
                        "supplier_name": preview.supplier_name,
                        "ean": parsed["ean"],
                        "base_unit_cost": str(landed.get("base_unit_cost", parsed["unit_cost"])),
                        "allocated_inbound_shipping": str(landed.get("allocated_inbound_shipping", Decimal("0"))),
                        "allocated_inbound_shipping_per_unit": str(landed.get("allocated_inbound_shipping_per_unit", Decimal("0"))),
                        "landed_cost_allocation": str(landed.get("landed_cost_allocation", LANDED_ALLOCATION_LABELS[allocation_method])),
                        "raw_row": raw_row,
                    },
                )
            )

    await db.commit()
    await db.refresh(invoice)
    return invoice
