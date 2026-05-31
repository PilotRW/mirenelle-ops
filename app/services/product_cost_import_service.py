from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ingestion.product_costs import ProductCostPreview, calculate_sha256
from app.models.product_cost import ProductCost
from app.models.product_cost_import import ProductCostImport
from app.services.amazon_payment_import_service import DuplicateImportError


async def commit_product_cost_import(
    db: AsyncSession,
    content: bytes,
    preview: ProductCostPreview,
) -> ProductCostImport:
    source_sha256 = calculate_sha256(content)

    existing = await db.scalar(
        select(ProductCostImport).where(ProductCostImport.source_sha256 == source_sha256)
    )
    if existing:
        raise DuplicateImportError(existing.id)

    cost_import = ProductCostImport(
        source_filename=preview.filename,
        source_sha256=source_sha256,
        currency=preview.currency,
        effective_date=preview.effective_date,
        header_mapping=preview.mapping,
        row_count=len(preview.parsed_rows),
    )
    db.add(cost_import)
    await db.flush()

    for raw_row, parsed_row in zip(preview.raw_rows, preview.parsed_rows):
        db.add(
            ProductCost(
                import_id=cost_import.id,
                sku=str(parsed_row["sku"]),
                product_name=str(parsed_row["product_name"] or "") or None,
                purchase_cost=parsed_row["purchase_cost"],
                currency=str(parsed_row["currency"]),
                effective_date=parsed_row["effective_date"],
                raw_row=raw_row,
            )
        )

    await db.commit()
    await db.refresh(cost_import)
    return cost_import

