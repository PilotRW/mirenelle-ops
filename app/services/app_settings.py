import json
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.app_setting import AppSetting


LANDED_COST_ALLOCATION_METHOD_KEY = "landed_cost_allocation_method"
LANDED_COST_ALLOCATION_METHODS = {"by_quantity", "by_line_value"}
DEFAULT_LANDED_COST_ALLOCATION_METHOD = "by_quantity"
FULFILLMENT_COST_SETTING_KEYS = {
    "fba_prep_per_unit": "fulfillment_cost_fba_prep_per_unit",
    "fba_storage_per_unit": "fulfillment_cost_fba_storage_per_unit",
    "fbm_prep_per_unit": "fulfillment_cost_fbm_prep_per_unit",
    "fbm_packaging_per_unit": "fulfillment_cost_fbm_packaging_per_unit",
    "fbm_outbound_per_unit": "fulfillment_cost_fbm_outbound_per_unit",
    "fbm_storage_per_unit": "fulfillment_cost_fbm_storage_per_unit",
}
PAYMENTS_SYNC_CONFIG_KEY = "payments_sync_schedule_config"
PAYMENTS_SYNC_RUNTIME_KEY = "payments_sync_schedule_runtime"
DEFAULT_PAYMENTS_SYNC_CONFIG = {
    "enabled": False,
    "interval_hours": 24,
    "lookback_days": 14,
    "marketplaces": ["DE", "FR", "IT", "ES", "NL", "BE", "PL", "SE", "IE", "UK"],
}


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


async def get_fulfillment_cost_settings(db: AsyncSession) -> dict[str, float]:
    settings: dict[str, float] = {}
    for field, key in FULFILLMENT_COST_SETTING_KEYS.items():
        value = await get_setting(db, key, "0")
        try:
            settings[field] = max(float(value), 0.0)
        except ValueError:
            settings[field] = 0.0
    return settings


async def set_fulfillment_cost_settings(
    db: AsyncSession,
    values: dict[str, float],
) -> dict[str, float]:
    normalized = {
        field: max(float(values.get(field, 0)), 0.0)
        for field in FULFILLMENT_COST_SETTING_KEYS
    }
    for field, key in FULFILLMENT_COST_SETTING_KEYS.items():
        row = await db.get(AppSetting, key)
        if row is None:
            db.add(AppSetting(key=key, value=str(normalized[field])))
        else:
            row.value = str(normalized[field])
    await db.commit()
    return normalized


async def get_payments_sync_config(db: AsyncSession) -> dict:
    raw = await get_setting(
        db,
        PAYMENTS_SYNC_CONFIG_KEY,
        json.dumps(DEFAULT_PAYMENTS_SYNC_CONFIG),
    )
    try:
        saved = json.loads(raw)
    except (TypeError, ValueError):
        saved = {}
    return {
        "enabled": bool(saved.get("enabled", False)),
        "interval_hours": min(max(int(saved.get("interval_hours", 24)), 1), 168),
        "lookback_days": min(max(int(saved.get("lookback_days", 14)), 2), 90),
        "marketplaces": [
            str(value).upper()
            for value in saved.get("marketplaces", DEFAULT_PAYMENTS_SYNC_CONFIG["marketplaces"])
        ],
    }


async def set_payments_sync_config(db: AsyncSession, values: dict) -> dict:
    normalized = {
        "enabled": bool(values.get("enabled", False)),
        "interval_hours": min(max(int(values.get("interval_hours", 24)), 1), 168),
        "lookback_days": min(max(int(values.get("lookback_days", 14)), 2), 90),
        "marketplaces": sorted(
            {str(value).upper() for value in values.get("marketplaces", [])}
        ),
    }
    await set_setting(db, PAYMENTS_SYNC_CONFIG_KEY, json.dumps(normalized))
    return normalized


async def get_payments_sync_runtime(db: AsyncSession) -> dict:
    raw = await get_setting(db, PAYMENTS_SYNC_RUNTIME_KEY, "{}")
    try:
        return json.loads(raw)
    except (TypeError, ValueError):
        return {}


async def set_payments_sync_runtime(db: AsyncSession, values: dict) -> dict:
    runtime = {
        **values,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    await set_setting(db, PAYMENTS_SYNC_RUNTIME_KEY, json.dumps(runtime))
    return runtime
