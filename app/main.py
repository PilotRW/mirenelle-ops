import asyncio
from contextlib import asynccontextmanager, suppress

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
try:
    from starlette.middleware.sessions import SessionMiddleware
except ModuleNotFoundError:
    SessionMiddleware = None

from app.api import amazon_payments
from app.api import amazon_connector
from app.api import fx_rates
from app.api import health
from app.api import inventory
from app.api import mock_costs
from app.api import product_mappings
from app.api import product_costs
from app.api import purchase_invoices
from app.api import report_previews
from app.api import reports
from app.api import settings
from app.api import supplier_catalog
from app.auth.middleware import auth_middleware
from app.auth.routes import router as auth_router
from app.config.settings import settings as app_settings
from app.services.payments_sync_scheduler import payments_sync_scheduler_loop


@asynccontextmanager
async def lifespan(_app: FastAPI):
    scheduler_task = asyncio.create_task(payments_sync_scheduler_loop())
    yield
    scheduler_task.cancel()
    with suppress(asyncio.CancelledError):
        await scheduler_task


app = FastAPI(title="Mirenelle Ops", lifespan=lifespan)

app.middleware("http")(auth_middleware)
if SessionMiddleware is None:
    if app_settings.AUTH_ENABLED:
        raise RuntimeError("AUTH_ENABLED=true requires the itsdangerous package.")
else:
    app.add_middleware(
        SessionMiddleware,
        secret_key=app_settings.AUTH_SESSION_SECRET,
        same_site="lax",
        https_only=app_settings.AUTH_ENABLED,
    )

app.mount("/ui", StaticFiles(directory="app/static", html=True), name="ui")

app.include_router(auth_router)
app.include_router(amazon_payments.router)
app.include_router(amazon_connector.router)
app.include_router(fx_rates.router)
app.include_router(health.router)
app.include_router(inventory.router)
app.include_router(mock_costs.router)
app.include_router(product_mappings.router)
app.include_router(product_costs.router)
app.include_router(purchase_invoices.router)
app.include_router(report_previews.router)
app.include_router(reports.router)
app.include_router(settings.router)
app.include_router(supplier_catalog.router)


@app.get("/")
async def root():
    return RedirectResponse(url="/ui/")
