from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.api import amazon_payments
from app.api import fx_rates
from app.api import health
from app.api import mock_costs
from app.api import product_mappings
from app.api import product_costs
from app.api import purchase_invoices
from app.api import report_previews
from app.api import reports
from app.api import supplier_catalog


app = FastAPI(title="Mirenelle Ops")

app.mount("/ui", StaticFiles(directory="app/static", html=True), name="ui")

app.include_router(amazon_payments.router)
app.include_router(fx_rates.router)
app.include_router(health.router)
app.include_router(mock_costs.router)
app.include_router(product_mappings.router)
app.include_router(product_costs.router)
app.include_router(purchase_invoices.router)
app.include_router(report_previews.router)
app.include_router(reports.router)
app.include_router(supplier_catalog.router)


@app.get("/")
async def root():
    return RedirectResponse(url="/ui/")
