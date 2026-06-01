from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.services.supplier_catalog_service import (
    supplier_catalog_stats,
    sync_supplier_catalog_from_oa,
)


router = APIRouter(prefix="/integrations/oa-pipeline/catalog", tags=["supplier-catalog"])


class SupplierCatalogStatsResponse(BaseModel):
    items: int
    with_ean: int
    last_synced_at: str | None


class SupplierCatalogSyncResponse(SupplierCatalogStatsResponse):
    imported_count: int


@router.get("", response_model=SupplierCatalogStatsResponse)
async def get_supplier_catalog_stats(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> SupplierCatalogStatsResponse:
    return SupplierCatalogStatsResponse(**await supplier_catalog_stats(db))


@router.post("/sync", response_model=SupplierCatalogSyncResponse)
async def sync_supplier_catalog(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> SupplierCatalogSyncResponse:
    try:
        result = await sync_supplier_catalog_from_oa(db)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    stats = await supplier_catalog_stats(db)
    return SupplierCatalogSyncResponse(
        imported_count=result.imported_count,
        **stats,
    )
