from datetime import date
from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.models.fx_rate import FxRate
from app.services.fx import get_latest_fx_rates


router = APIRouter(prefix="/settings/fx-rates", tags=["fx-rates"])


class FxRateRow(BaseModel):
    id: int | None = None
    currency: str
    rate_to_eur: float
    effective_date: str


class FxRateListResponse(BaseModel):
    rows: list[FxRateRow]


class FxRateCreateRequest(BaseModel):
    currency: str = Field(min_length=3, max_length=8)
    rate_to_eur: Decimal = Field(gt=0)
    effective_date: date


@router.get("", response_model=FxRateListResponse)
async def list_fx_rates(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> FxRateListResponse:
    result = await db.scalars(
        select(FxRate).order_by(FxRate.currency, FxRate.effective_date.desc(), FxRate.id.desc())
    )
    return FxRateListResponse(
        rows=[
            FxRateRow(
                id=row.id,
                currency=row.currency,
                rate_to_eur=float(row.rate_to_eur),
                effective_date=row.effective_date.isoformat(),
            )
            for row in result
        ]
    )


@router.get("/latest", response_model=FxRateListResponse)
async def latest_fx_rates(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> FxRateListResponse:
    rates = await get_latest_fx_rates(db)
    return FxRateListResponse(
        rows=[
            FxRateRow(
                currency=currency,
                rate_to_eur=float(rate),
                effective_date="latest",
            )
            for currency, rate in sorted(rates.items())
        ]
    )


@router.post("", response_model=FxRateRow)
async def create_fx_rate(
    payload: FxRateCreateRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> FxRateRow:
    currency = payload.currency.upper()
    existing = await db.scalar(
        select(FxRate).where(
            FxRate.currency == currency,
            FxRate.effective_date == payload.effective_date,
        )
    )
    if existing:
        raise HTTPException(
            status_code=409,
            detail=f"FX rate for {currency} on {payload.effective_date.isoformat()} already exists.",
        )

    row = FxRate(
        currency=currency,
        rate_to_eur=payload.rate_to_eur,
        effective_date=payload.effective_date,
    )
    db.add(row)
    await db.commit()
    await db.refresh(row)
    return FxRateRow(
        id=row.id,
        currency=row.currency,
        rate_to_eur=float(row.rate_to_eur),
        effective_date=row.effective_date.isoformat(),
    )

