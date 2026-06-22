from typing import Annotated, Literal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.services.app_settings import (
    LANDED_COST_ALLOCATION_METHODS,
    get_fulfillment_cost_settings,
    get_landed_cost_allocation_method,
    get_payments_sync_config,
    get_payments_sync_runtime,
    set_fulfillment_cost_settings,
    set_landed_cost_allocation_method,
    set_payments_sync_config,
)
from app.services.amazon_sp_api_client import MARKETPLACE_IDS
from app.services.payments_sync_scheduler import run_scheduled_payments_sync


router = APIRouter(prefix="/settings", tags=["settings"])


LandedCostAllocationMethod = Literal["by_quantity", "by_line_value"]


class LandedCostSettingsResponse(BaseModel):
    allocation_method: LandedCostAllocationMethod
    available_methods: list[str]


class LandedCostSettingsUpdateRequest(BaseModel):
    allocation_method: LandedCostAllocationMethod


class FulfillmentCostSettings(BaseModel):
    currency: str = "EUR"
    fba_prep_per_unit: float = Field(ge=0)
    fba_storage_per_unit: float = Field(ge=0)
    fbm_prep_per_unit: float = Field(ge=0)
    fbm_packaging_per_unit: float = Field(ge=0)
    fbm_outbound_per_unit: float = Field(ge=0)
    fbm_storage_per_unit: float = Field(ge=0)


class PaymentsSyncScheduleSettings(BaseModel):
    enabled: bool = False
    interval_hours: int = Field(default=24, ge=1, le=168)
    lookback_days: int = Field(default=14, ge=2, le=90)
    marketplaces: list[str]


class PaymentsSyncScheduleResponse(PaymentsSyncScheduleSettings):
    available_marketplaces: list[str]
    runtime: dict


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


@router.get("/fulfillment-costs", response_model=FulfillmentCostSettings)
async def get_fulfillment_costs(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> FulfillmentCostSettings:
    return FulfillmentCostSettings(
        **await get_fulfillment_cost_settings(db),
    )


@router.put("/fulfillment-costs", response_model=FulfillmentCostSettings)
async def update_fulfillment_costs(
    payload: FulfillmentCostSettings,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> FulfillmentCostSettings:
    values = payload.model_dump(exclude={"currency"})
    return FulfillmentCostSettings(
        **await set_fulfillment_cost_settings(db, values),
    )


@router.get("/payments-sync-schedule", response_model=PaymentsSyncScheduleResponse)
async def get_payments_sync_schedule(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> PaymentsSyncScheduleResponse:
    return PaymentsSyncScheduleResponse(
        **await get_payments_sync_config(db),
        available_marketplaces=sorted(MARKETPLACE_IDS),
        runtime=await get_payments_sync_runtime(db),
    )


@router.put("/payments-sync-schedule", response_model=PaymentsSyncScheduleResponse)
async def update_payments_sync_schedule(
    payload: PaymentsSyncScheduleSettings,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> PaymentsSyncScheduleResponse:
    invalid = sorted(set(payload.marketplaces) - set(MARKETPLACE_IDS))
    if invalid:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported marketplaces: {', '.join(invalid)}",
        )
    if payload.enabled and not payload.marketplaces:
        raise HTTPException(
            status_code=400,
            detail="Select at least one marketplace before enabling automatic sync.",
        )
    config = await set_payments_sync_config(db, payload.model_dump())
    return PaymentsSyncScheduleResponse(
        **config,
        available_marketplaces=sorted(MARKETPLACE_IDS),
        runtime=await get_payments_sync_runtime(db),
    )


@router.post("/payments-sync-schedule/run")
async def run_payments_sync_schedule_now() -> dict:
    return await run_scheduled_payments_sync(force=True)
