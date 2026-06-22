import asyncio
from datetime import date, datetime, timedelta, timezone

from app.db.database import AsyncSessionLocal
from app.services.amazon_finances_sync_service import (
    AmazonFinancesSyncConflict,
    sync_finance_transactions,
)
from app.services.app_settings import (
    get_payments_sync_config,
    get_payments_sync_runtime,
    set_payments_sync_runtime,
)


_sync_lock = asyncio.Lock()


def _parse_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


async def run_scheduled_payments_sync(force: bool = False) -> dict:
    if _sync_lock.locked():
        return {"status": "already_running"}

    async with _sync_lock:
        async with AsyncSessionLocal() as db:
            config = await get_payments_sync_config(db)
            runtime = await get_payments_sync_runtime(db)
            if not force and not config["enabled"]:
                return {"status": "disabled"}

            now = datetime.now(timezone.utc)
            last_attempt = _parse_datetime(runtime.get("last_attempt_at"))
            if (
                not force
                and last_attempt
                and now - last_attempt < timedelta(hours=config["interval_hours"])
            ):
                return {"status": "not_due"}

            end_date = date.today()
            start_date = end_date - timedelta(days=config["lookback_days"] - 1)
            await set_payments_sync_runtime(
                db,
                {
                    **runtime,
                    "running": True,
                    "last_attempt_at": now.isoformat(),
                    "last_error": None,
                },
            )

        results = []
        errors = []
        for marketplace in config["marketplaces"]:
            async with AsyncSessionLocal() as db:
                try:
                    result = await sync_finance_transactions(
                        db,
                        marketplace,
                        start_date,
                        end_date,
                    )
                    results.append(
                        {
                            "marketplace": marketplace,
                            "status": result.status,
                            "transactions_received": result.transactions_received,
                            "rows_imported": result.rows_imported,
                            "rows_updated": result.rows_updated,
                            "rows_skipped": result.rows_skipped,
                        }
                    )
                except AmazonFinancesSyncConflict as exc:
                    errors.append({"marketplace": marketplace, "error": str(exc)})
                except Exception as exc:  # scheduler must continue with other markets
                    errors.append({"marketplace": marketplace, "error": str(exc)})

        finished_at = datetime.now(timezone.utc).isoformat()
        runtime = {
            "running": False,
            "last_attempt_at": now.isoformat(),
            "last_finished_at": finished_at,
            "last_success_at": finished_at if results else runtime.get("last_success_at"),
            "period_start": start_date.isoformat(),
            "period_end": end_date.isoformat(),
            "results": results,
            "errors": errors,
            "last_error": errors[0]["error"] if errors and not results else None,
        }
        async with AsyncSessionLocal() as db:
            await set_payments_sync_runtime(db, runtime)
        return {"status": "completed", **runtime}


async def payments_sync_scheduler_loop() -> None:
    while True:
        try:
            await run_scheduled_payments_sync()
        except asyncio.CancelledError:
            raise
        except Exception:
            # Runtime details are persisted by the run whenever possible. The
            # loop itself must survive a transient database or Amazon failure.
            pass
        await asyncio.sleep(60)
