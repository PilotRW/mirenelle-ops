import asyncio
import csv
from datetime import date
from decimal import Decimal
from io import StringIO
from typing import Annotated
from urllib.request import urlopen

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


class EcbSyncRequest(BaseModel):
    start_date: date | None = None
    end_date: date | None = None
    currencies: list[str] = Field(default_factory=lambda: ["SEK", "GBP", "PLN"])


class EcbSyncResponse(BaseModel):
    source: str
    rows_upserted: int
    start_date: str | None
    end_date: str | None
    currencies: list[str]


ECB_DATA_API_URL = "https://data-api.ecb.europa.eu/service/data/EXR"


def download_ecb_history(
    currency: str,
    start_date: date | None,
    end_date: date | None,
) -> str:
    parameters = ["format=csvdata"]
    if start_date:
        parameters.append(f"startPeriod={start_date.isoformat()}")
    if end_date:
        parameters.append(f"endPeriod={end_date.isoformat()}")
    url = (
        f"{ECB_DATA_API_URL}/D.{currency}.EUR.SP00.A"
        f"?{'&'.join(parameters)}"
    )
    with urlopen(url, timeout=30) as response:
        return response.read().decode("utf-8-sig")


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


@router.post("/sync-ecb", response_model=EcbSyncResponse)
async def sync_ecb_rates(
    payload: EcbSyncRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> EcbSyncResponse:
    currencies = sorted({currency.strip().upper() for currency in payload.currencies if currency.strip()})
    rows_upserted = 0
    for currency in currencies:
        try:
            content = await asyncio.to_thread(
                download_ecb_history,
                currency,
                payload.start_date,
                payload.end_date,
            )
        except Exception as exc:
            raise HTTPException(
                status_code=502,
                detail=f"ECB download failed for {currency}: {exc}",
            ) from exc
        for raw in csv.DictReader(StringIO(content)):
            rate_date = date.fromisoformat(raw["TIME_PERIOD"])
            raw_rate = (raw.get("OBS_VALUE") or "").strip()
            if not raw_rate:
                continue
            # ECB publishes 1 EUR = X foreign currency. Mirenelle stores
            # foreign currency -> EUR, so the stored rate is the inverse.
            rate_to_eur = (Decimal("1") / Decimal(raw_rate)).quantize(Decimal("0.00000001"))
            existing = await db.scalar(
                select(FxRate).where(
                    FxRate.currency == currency,
                    FxRate.effective_date == rate_date,
                )
            )
            if existing is None:
                db.add(
                    FxRate(
                        currency=currency,
                        rate_to_eur=rate_to_eur,
                        effective_date=rate_date,
                    )
                )
            else:
                existing.rate_to_eur = rate_to_eur
            rows_upserted += 1
    await db.commit()
    return EcbSyncResponse(
        source="ECB",
        rows_upserted=rows_upserted,
        start_date=payload.start_date.isoformat() if payload.start_date else None,
        end_date=payload.end_date.isoformat() if payload.end_date else None,
        currencies=currencies,
    )
