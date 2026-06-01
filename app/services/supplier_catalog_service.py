from dataclasses import dataclass

from sqlalchemy import delete, func, select, text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from app.config.settings import settings
from app.ingestion.amazon_reports.header_aliases import normalize_header
from app.models.supplier_catalog_item import SupplierCatalogItem


@dataclass(frozen=True)
class CatalogSyncResult:
    imported_count: int
    with_ean_count: int
    source: str = "oa_pipeline"


def normalize_key(value: str | None) -> str:
    return normalize_header(value or "")


async def sync_supplier_catalog_from_oa(db: AsyncSession) -> CatalogSyncResult:
    if not settings.OA_DATABASE_URL:
        raise ValueError("OA_DATABASE_URL is not configured.")

    engine = create_async_engine(settings.OA_DATABASE_URL)
    try:
        async with engine.connect() as connection:
            result = await connection.execute(
                text(
                    """
                    select
                        so.id as source_offer_id,
                        s.name as supplier_name,
                        so.supplier_sku,
                        so.ean,
                        so.brand,
                        so.title,
                        so.cost,
                        so.currency,
                        so.imported_at as source_imported_at,
                        so.raw_data
                    from supplier_offers so
                    left join suppliers s on s.id = so.supplier_id
                    where coalesce(so.supplier_sku, '') != ''
                       or coalesce(so.ean, '') != ''
                       or coalesce(so.title, '') != ''
                    """
                )
            )
            rows = result.mappings().all()
    finally:
        await engine.dispose()

    await db.execute(delete(SupplierCatalogItem).where(SupplierCatalogItem.source == "oa_pipeline"))
    db.add_all(
        [
            SupplierCatalogItem(
                source="oa_pipeline",
                source_offer_id=row["source_offer_id"],
                supplier_name=row["supplier_name"],
                supplier_sku=row["supplier_sku"],
                ean=row["ean"],
                brand=row["brand"],
                title=row["title"],
                cost=row["cost"],
                currency=row["currency"],
                source_imported_at=row["source_imported_at"],
                raw_data=row["raw_data"],
            )
            for row in rows
        ]
    )
    await db.commit()
    return CatalogSyncResult(
        imported_count=len(rows),
        with_ean_count=sum(1 for row in rows if row["ean"]),
    )


async def supplier_catalog_stats(db: AsyncSession) -> dict[str, int | str | None]:
    result = await db.execute(
        select(
            func.count(SupplierCatalogItem.id).label("items"),
            func.count(SupplierCatalogItem.ean).label("with_ean"),
            func.max(SupplierCatalogItem.synced_at).label("last_synced_at"),
        )
    )
    row = result.one()
    last_synced_at = row.last_synced_at
    return {
        "items": int(row.items or 0),
        "with_ean": int(row.with_ean or 0),
        "last_synced_at": last_synced_at.isoformat() if last_synced_at else None,
    }


async def enrich_invoice_rows_from_catalog(
    db: AsyncSession,
    supplier_name: str,
    parsed_rows: list[dict],
) -> int:
    product_rows = [row for row in parsed_rows if row.get("line_type") == "product" and not row.get("ean")]
    if not product_rows:
        return 0

    sku_values = {
        str(value).strip()
        for row in product_rows
        for value in (row.get("sku"), row.get("supplier_sku"))
        if value
    }
    if not sku_values:
        return 0

    result = await db.scalars(
        select(SupplierCatalogItem)
        .where(SupplierCatalogItem.ean.is_not(None))
        .where(SupplierCatalogItem.ean != "")
        .where(SupplierCatalogItem.supplier_sku.in_(sku_values))
        .order_by(SupplierCatalogItem.source_imported_at.desc().nullslast(), SupplierCatalogItem.id.desc())
    )
    catalog_items = result.all()

    supplier_key = normalize_key(supplier_name)
    scoped_by_sku: dict[str, SupplierCatalogItem] = {}
    global_by_sku: dict[str, SupplierCatalogItem] = {}
    for item in catalog_items:
        if not item.supplier_sku:
            continue
        sku_key = str(item.supplier_sku).strip()
        global_by_sku.setdefault(sku_key, item)
        if supplier_key and normalize_key(item.supplier_name) == supplier_key:
            scoped_by_sku.setdefault(sku_key, item)

    enriched = 0
    for row in product_rows:
        candidates = [str(value).strip() for value in (row.get("sku"), row.get("supplier_sku")) if value]
        item = next((scoped_by_sku.get(value) for value in candidates if scoped_by_sku.get(value)), None)
        item = item or next((global_by_sku.get(value) for value in candidates if global_by_sku.get(value)), None)
        if item and item.ean:
            row["ean"] = item.ean
            row.setdefault("catalog_source", "oa_pipeline")
            row.setdefault("catalog_source_offer_id", item.source_offer_id)
            enriched += 1

    return enriched
