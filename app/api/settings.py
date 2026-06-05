from typing import Annotated, Literal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.services.app_settings import (
    LANDED_COST_ALLOCATION_METHODS,
    get_landed_cost_allocation_method,
    set_landed_cost_allocation_method,
)


router = APIRouter(prefix="/settings", tags=["settings"])


LandedCostAllocationMethod = Literal["by_quantity", "by_line_value"]


class LandedCostSettingsResponse(BaseModel):
    allocation_method: LandedCostAllocationMethod
    available_methods: list[str]


class LandedCostSettingsUpdateRequest(BaseModel):
    allocation_method: LandedCostAllocationMethod


@router.get("/landed-cost", response_model=LandedCostSettingsResponse)
async def get_landed_cost_settings(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> LandedCostSettingsResponse:
    return LandedCostSettingsResponse(
        allocation_method=await get_landed_cost_allocation_method(db),
        available_methods=sorted(LANDED_COST_ALLOCATION_METHODS),
    )


@router.put("/landed-cost", response_model=LandedCostSettingsResponse)
async def update_landed_cost_settings(
    payload: LandedCostSettingsUpdateRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> LandedCostSettingsResponse:
    try:
        await set_landed_cost_allocation_method(db, payload.allocation_method)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return LandedCostSettingsResponse(
        allocation_method=payload.allocation_method,
        available_methods=sorted(LANDED_COST_ALLOCATION_METHODS),
    )
