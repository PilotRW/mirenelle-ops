from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.fx_rate import FxRate


FX_TO_EUR: dict[str, Decimal] = {
    "EUR": Decimal("1.000000"),
    "SEK": Decimal("0.087000"),
    "GBP": Decimal("1.170000"),
    "PLN": Decimal("0.235000"),
}


def convert_to_eur_with_rate(amount: Decimal | int | float | None, rate_to_eur: Decimal) -> Decimal:
    if amount is None:
        return Decimal("0")
    value = amount if isinstance(amount, Decimal) else Decimal(str(amount))
    return (value * rate_to_eur).quantize(Decimal("0.01"))


def convert_to_eur(amount: Decimal | int | float | None, currency: str) -> Decimal:
    rate_to_eur = FX_TO_EUR.get(currency.upper())
    if rate_to_eur is None:
        raise ValueError(f"Missing FX rate to EUR for {currency}")
    return convert_to_eur_with_rate(amount, rate_to_eur)


async def get_latest_fx_rates(db: AsyncSession) -> dict[str, Decimal]:
    result = await db.execute(
        select(FxRate).order_by(FxRate.currency, FxRate.effective_date.desc(), FxRate.id.desc())
    )
    rates: dict[str, Decimal] = {}
    for row in result.scalars():
        rates.setdefault(row.currency.upper(), row.rate_to_eur)
    return rates


def get_rate_for_currency(rates: dict[str, Decimal], currency: str) -> Decimal:
    rate_to_eur = rates.get(currency.upper())
    if rate_to_eur is None:
        raise ValueError(f"Missing FX rate to EUR for {currency}")
    return rate_to_eur

