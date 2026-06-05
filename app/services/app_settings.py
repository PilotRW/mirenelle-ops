from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.app_setting import AppSetting


LANDED_COST_ALLOCATION_METHOD_KEY = "landed_cost_allocation_method"
LANDED_COST_ALLOCATION_METHODS = {"by_quantity", "by_line_value"}
DEFAULT_LANDED_COST_ALLOCATION_METHOD = "by_quantity"


async def get_setting(
    db: AsyncSession,
    key: str,
    default: str,
) -> str:
    row = await db.get(AppSetting, key)
    return row.value if row else default


async def set_setting(
    db: AsyncSession,
    key: str,
    value: str,
) -> AppSetting:
    row = await db.get(AppSetting, key)
    if row is None:
        row = AppSetting(key=key, value=value)
        db.add(row)
    else:
        row.value = value
    await db.commit()
    await db.refresh(row)
    return row


async def get_landed_cost_allocation_method(db: AsyncSession) -> str:
    value = await get_setting(
        db,
        LANDED_COST_ALLOCATION_METHOD_KEY,
        DEFAULT_LANDED_COST_ALLOCATION_METHOD,
    )
    if value not in LANDED_COST_ALLOCATION_METHODS:
        return DEFAULT_LANDED_COST_ALLOCATION_METHOD
    return value


async def set_landed_cost_allocation_method(db: AsyncSession, value: str) -> AppSetting:
    if value not in LANDED_COST_ALLOCATION_METHODS:
        raise ValueError("Unsupported landed cost allocation method.")
    return await set_setting(db, LANDED_COST_ALLOCATION_METHOD_KEY, value)
