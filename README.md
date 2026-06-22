# Mirenelle Ops

Operations, accounting, inventory, and forecasting service for Mirenelle.

This project is separate from `oa-pipeline`. OA Pipeline finds supplier and
Amazon deal candidates; Mirenelle Ops tracks what happened operationally:
Amazon transactions, product costs, inventory movements, cashflow, stock
forecasting, and replenishment recommendations.

## Current Scope

Initial MVP:

- Import Amazon Payments Transaction View CSV files.
- Sync posted Payments automatically through Amazon Finances API v2024-06-19.
- Support European Seller Central localizations through explicit header aliases.
- Store raw rows and normalized ledger rows.
- Keep marketplace reports in the original sale currency.
- Convert general/consolidated reports to EUR.
- Prepare for product cost catalog import.
- Prepare for future integration with `oa-pipeline` through API/export, not
  shared tables.

## Database

Use a separate database from OA Pipeline, ideally on the same local Postgres
instance:

```text
postgresql+asyncpg://oa:oa@localhost:5432/mirenelle_ops
```

OA Pipeline keeps using:

```text
postgresql+asyncpg://oa:oa@localhost:5432/oa
```

## Planned Flow

```text
Upload Amazon report
  -> detect report type
  -> detect locale/header mapping
  -> preview
  -> validate
  -> commit raw rows
  -> normalize accounting ledger
  -> marketplace/month dashboard
```

## API

Local operator UI:

```text
http://localhost:8010/ui/
```

The UI supports English, German, and Ukrainian through the language selector in
the top bar.

Health:

```text
GET /health
```

Preview Amazon Payments Transaction View CSV:

```text
POST /imports/amazon-payments/preview
```

Commit Amazon Payments Transaction View CSV:

```text
POST /imports/amazon-payments/commit
```

List Amazon Payments imports:

```text
GET /imports/amazon-payments
```

Sync Payments directly from Amazon:

```text
POST /integrations/amazon-sp-api/payments/sync
```

Automatic Payments sync is configured in `Settings -> Payments Automation`.
It is disabled by default. The operator can select marketplaces, the run
interval (1-168 hours), and a rolling overlap window (2-90 days). The overlap
is intentional: Finances event IDs make repeated periods idempotent, while the
window allows deferred transactions to be replaced by their final released
state. The panel also shows the last run result and provides `Run now`.

```text
GET  /settings/payments-sync-schedule
PUT  /settings/payments-sync-schedule
POST /settings/payments-sync-schedule/run
```

The payload contains `marketplace`, `start_date`, and `end_date`. Finance event
IDs are stored on payment rows, so repeated or overlapping API syncs skip rows
already imported. A Finances API sync is blocked when the requested period
overlaps a manual CSV import for the same marketplace; delete the manual import
first if the intention is to replace it.

Amazon may expose the same financial operation first as `DEFERRED_RELEASED`
and later as `RELEASED`. Both lifecycle records resolve to one canonical event
ID. When the final state arrives later, the existing row is updated instead of
creating a second sale.

Multipart form fields:

```text
file: CSV file
marketplace: optional marketplace code, for example DE or SE
sample_size: optional preview row count, 1-50, default 10
```

The preview endpoint does not write to the database. It returns detected
headers, canonical mapping, missing/ambiguous/unknown headers, detected
currency, sample rows, normalized sample rows, and totals by transaction type.

Duplicate files are blocked by SHA-256 fingerprint.

Preview and commit product cost catalog:

```text
POST /imports/product-costs/preview
POST /imports/product-costs/commit
GET  /imports/product-costs
```

Preview and commit purchase invoices:

```text
POST /imports/purchase-invoices/preview
POST /imports/purchase-invoices/commit
GET  /imports/purchase-invoices
GET  /imports/purchase-invoices/{invoice_id}/lines
```

The invoice importer stores document-level metadata and line-level purchase
data. It also writes invoice line unit costs into `product_costs`, so product
profitability can use real invoice costs as soon as they are imported.
Supported invoice file types are CSV, XLSX/XLS, and text-based PDF. PDF import
extracts supplier, invoice number, invoice date, product lines, EAN, quantity,
VAT, unit cost, net amount, computed VAT amount, and computed gross amount when
those fields are present in the text layer.

Invoice lines are classified before commit. Product lines create product costs;
transport, fulfillment, marketplace fees, and service rows stay as separate
expense lines for purchase/cashflow reporting and future landed-cost allocation.

Product mappings connect supplier invoice lines to Amazon transaction product
names when the names are not identical:

```text
GET  /product-mappings
GET  /product-mappings/suggestions
POST /product-mappings
```

Suggestions compare unmapped invoice lines with sold Amazon products and can be
confirmed from the UI. Confirmed mappings are used by product profitability.

Initial product cost catalog fields:

```text
Nazwa produktu
SKU
Zakup EUR / Zakup €
```

Reports:

```text
GET /reports/monthly-cashflow
GET /reports/product-costs/latest
GET /reports/product-profitability
GET /reports/purchase-summary
```

`GET /reports/data-quality` reconciles sale and refund ledger groups against
Amazon Orders. Sale and refund matching uses exact Amazon Order ID + SKU.
Amazon return-fee rows use technical `X00...` SKUs; they receive a linked
product SKU only when the same order contains exactly one refunded product.
Orders with multiple refunded SKUs are reported as ambiguous and are never
assigned heuristically.

Read-only FBA Customer Returns sync:

```text
POST /integrations/amazon-sp-api/returns/sync
GET  /integrations/amazon-sp-api/returns/imports
```

The importer uses Amazon report
`GET_FBA_FULFILLMENT_CUSTOMER_RETURNS_DATA`. It stores order ID, seller SKU,
ASIN, FNSKU, disposition, reason, status, fulfillment center, LPN, and customer
comments. FNSKU provides the exact bridge from Payments technical return-fee
SKUs (`X00...`) to the real product SKU. Matched return fees are included in
the corresponding Product Profitability row.

Read-only FBA inventory sync:

```text
POST /integrations/amazon-sp-api/inventory/sync
```

The connector uses `GET_FBA_MYI_UNSUPPRESSED_INVENTORY_DATA`. Each sync stores
a timestamped snapshot and updates FBA Inventory rows. Amazon fulfillable
quantity becomes available stock, reserved and inbound quantities remain
separate, and unsellable/researching quantities remain available in snapshot
history without being counted as sellable stock. FIFO purchase lots remain the
accounting source for COGS and are not overwritten by Amazon stock snapshots.

Fulfillment cost settings:

```text
GET /settings/fulfillment-costs
PUT /settings/fulfillment-costs
```

These settings hold EUR-per-sold-unit rates for FBA prep/storage and FBM
prep, packaging, outbound logistics, and storage. They are shown separately
from COGS and Amazon fees in Product Profitability and reduce net profit.
Storage is currently an estimated allocation per sold unit; warehouse-day
storage will replace it after inventory snapshots are available.

Product COGS uses FIFO inventory lots created from purchase invoice product
lines. Each lot preserves its invoice date, received quantity, and landed unit
cost. Profitability consumes all historical sales chronologically through the
report end date, so older stock carries into later months and is exhausted
before newer, differently priced stock. Products without enough dated lots are
shown as missing cost rather than being assigned a future/latest invoice price.

The Product Costs page is a FIFO lot registry rather than a latest-price list.
It shows every acquisition lot, including repeated purchases of the same SKU,
with purchase date, received quantity, base unit cost, allocated inbound
shipping per unit, landed unit cost, currency, source, supplier, and invoice.

Opening stock that predates imported invoices can be entered from the Inventory
page or through:

```text
GET    /inventory/opening-lots
POST   /inventory/opening-lots
DELETE /inventory/opening-lots/{lot_id}
```

An opening lot requires the Amazon SKU, stock date, quantity, landed unit cost,
and currency. It participates in FIFO immediately and is included in purchased
inventory quantities.

Bundle recipes can also be configured on the Inventory page:

```text
GET    /inventory/bundle-components
POST   /inventory/bundle-components
POST   /inventory/bundle-recipes
DELETE /inventory/bundle-components/{component_id}
GET    /inventory/bundle-assemblies
POST   /inventory/bundle-assemblies
PUT    /inventory/bundle-assemblies/{assembly_id}
DELETE /inventory/bundle-assemblies/{assembly_id}
```

Each recipe maps a sold Amazon bundle SKU to one or more component SKU/EAN
values and quantities per sold bundle. FIFO consumes all recipe components
atomically. If any component is unavailable, the bundle remains missing cost
instead of receiving partial COGS.

The UI uses a draft workflow. Choose or type the sold Amazon bundle SKU, add
each component and quantity with `Add component`, then persist the complete
recipe with `Save bundle`. `Add component` does not write to the database.
`POST /inventory/bundle-recipes` replaces the complete recipe atomically, so
editing an existing bundle cannot leave a partially saved component list.

Inventory expands sold bundle quantities into their component quantities. A
bundle sale therefore reduces component stock even before historical assembly
operations are entered.

Bundle Assemblies records the physical transfer from loose components into
finished bundles. Each assembly stores its own recipe snapshot, date, quantity,
assembler (prep center by default, `unknown`, Amazon, in-house, or other), unit
assembly cost, currency, and notes. This prevents later recipe edits from changing
historical assembly consumption. Recorded assemblies cover bundle sales rather
than adding to them:
if 17 bundles were assembled and 4 later sold, components are consumed 17
times, not 21. If no assembly has been recorded, sold bundles continue to
consume components as a safe fallback.

Assembly cost is a separate operational cost rather than component COGS.
Product Profitability allocates it to sold bundles from the oldest eligible
assembly batches first. An assembly dated after a sale is never charged to that
sale. Non-EUR assembly cost is converted using the rate on the assembly date.
Saved assembly metadata can be edited in place. Quantity remains immutable
during editing because changing a physical assembly quantity is an inventory
movement; reverse the incorrect operation and record the corrected quantity
instead.

Product Profitability also creates a product row for a refund whose original
sale is outside the selected period when the refund can be linked by exact
Amazon Order ID + SKU. Such a row has zero period sales and zero period COGS;
the refund, promotional adjustment, and linked Amazon fees still affect period
net profit. Unmatched technical return-fee SKUs remain excluded.
Bundle SKU suggestions come from positive-quantity Amazon Orders rows and are
filtered only after the operator types at least two characters.

Example complete-recipe payload:

```json
{
  "bundle_sku": "AMAZON-BUNDLE-SKU",
  "bundle_name": "Confirmed bundle name",
  "components": [
    {"component_sku": "COMPONENT-1", "component_quantity": 1},
    {"component_sku": "COMPONENT-2", "component_quantity": 2}
  ]
}
```

Analytics reports accept optional date filters:

```text
?start_date=2026-05-01&end_date=2026-05-31
```

The UI exposes this as a dashboard period selector with all-time, this-month,
last-month, and custom ranges.

Marketplace rows in `/reports/monthly-cashflow` keep the original report
currency. The same response also includes `general_total_eur` for consolidated
EUR reporting. FX rates are operator-configurable through:

```text
GET  /settings/fx-rates
POST /settings/fx-rates
POST /settings/fx-rates/sync-ecb
```

ECB sync imports official daily reference rates from the ECB Data API. ECB
publishes `1 EUR = X foreign currency`; the importer stores the inverse as
`rate_to_eur`. Payments, refunds, fees, and order VAT use the rate effective on
their transaction date. Weekends and holidays fall back to the most recent
previous ECB business-day rate. Monthly reports aggregate only after each
transaction has been converted.

Generic report preview for shaping upcoming importers:

```text
POST /imports/report-preview
POST /imports/report-preview/commit
GET  /imports/report-preview
```

Supported preview report types:

```text
customer_returns
reimbursements
service_fees
```

The generic commit endpoint stores raw rows only. It is intended as a safe
holding area while canonical parsers for each report type are being built.

Mock cost generation for early analytics:

```text
POST /tools/mock-costs/from-transactions
```

This creates EUR product costs from current transaction product details using
`average product charges converted to EUR * cost_ratio`. It is deliberately
marked by the import filename `mock_from_transactions_*` so it can be replaced
by real purchase prices later.

## Purchase Invoice Fields

The importer tries to extract:

```text
supplier name
invoice number
invoice date
due date
currency
SKU / supplier SKU / EAN
product name
quantity
unit cost
line net amount
VAT rate
VAT amount
line gross amount
raw row
```

## First Canonical Report

Amazon Payments Transaction View:

```text
marketplace
currency
transaction_date
transaction_status
transaction_type
external_transaction_id
product_details
product_charges
promotional_rebates
amazon_fees
other_amount
total_amount
source_file
raw_row
```

Important: Transaction View exports may not include SKU, ASIN, or quantity.
SKU-level profit requires another Amazon order/item report or a reliable product
mapping source.

## Amazon SP-API Connector

The connector is read-only. It downloads Amazon reports and imports them into
local tables; it does not push or mutate anything in Amazon.

Required `.env` settings:

```env
AMAZON_SP_API_REFRESH_TOKEN=
AMAZON_SP_API_LWA_CLIENT_ID=
AMAZON_SP_API_LWA_CLIENT_SECRET=
AMAZON_SP_API_REGION=eu-west-1
AMAZON_SP_API_ENDPOINT=https://sellingpartnerapi-eu.amazon.com
```

Run the app after editing `.env`:

```bash
docker compose up -d --build
```

UI path:

```text
http://localhost:8010/ui/
```

Open `Amazon Connector` in the left sidebar, choose marketplace and period,
then click `Download orders`. The default marketplace option is `All EU
marketplaces`, which downloads DE, FR, IT, ES, NL, BE, PL, and SE one by one.
The UI calls:

```text
POST /integrations/amazon-sp-api/orders/sync
```

Current report type:

```text
GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_GENERAL
```

Amazon limits this order-tracking report range to 30 days. The connector
automatically splits longer UI periods into multiple report downloads and
imports them as one sync action.

The connector also uses a conservative Reports API throttle to avoid exceeding
Amazon limits. `createReport` is spaced at least 65 seconds apart across the
whole sync run, including `All EU marketplaces`; retryable Amazon responses
such as `429` and `503` are retried with backoff and `Retry-After` support.
The limiter is shared by Orders, Returns, FBA Inventory, Storage Fees, and
Reimbursements syncs, so starting different sync types at the same time does
not bypass the `createReport` interval.
This makes EU-wide sync intentionally slow but safer for API quotas.

Amazon report processing status `FATAL` is different from throttling: it means
Amazon failed to generate that specific report. Rate limiting is identified by
HTTP `429` / `QuotaExceeded`.

Manual All Orders report upload remains available on the same page as a
fallback/debug path.

## Dashboard Metrics

The dashboard and product profitability report calculate sellerboard-style
metrics from the currently available inputs:

- sales;
- orders / units;
- refunds;
- Amazon fees and other payment fees;
- COGS from purchase invoices/product costs;
- gross profit;
- net profit;
- margin and ROI;
- profitable/loss/breakeven product counts.

Ads, BSR, and forecast metrics are intentionally not mocked. They require PPC,
Keepa/catalog, or forecasting inputs and should be added as separate data
sources.

Reimbursements sync is available at
`POST /integrations/amazon-sp-api/reimbursements/sync`. It imports
`GET_FBA_REIMBURSEMENTS_DATA` with exact reimbursement-ID deduplication.
Reimbursements remain separate from sales revenue.

Product Profitability and Amazon P&L display reimbursements separately. They
use approval-date FX and affect Amazon operating result, but never sales, VAT,
units, average selling price, gross profit, or FIFO COGS. Product net profit
stays unknown if FIFO cost coverage is incomplete.

Prep-center tariffs are configured per SKU in
`Product Costs -> Prep-center tariffs by product`. Each SKU can have separate
FBA and FBM prep rates. Product Profitability uses the SKU-specific rate when
present and reports `prep_cost_source=product`; otherwise the global
Fulfillment Costs value remains an explicit `global_fallback`.

```text
GET    /settings/product-prep-costs
PUT    /settings/product-prep-costs/{sku}
DELETE /settings/product-prep-costs/{sku}
```

Detailed monthly FBA storage fees can be synced through
`POST /integrations/amazon-sp-api/storage-fees/sync`. The source is
`GET_FBA_STORAGE_FEE_CHARGES_DATA`; FNSKU is mapped through FBA inventory
snapshots. Single-month profitability uses the imported SKU-level fee instead
of the configured per-sold-unit estimate. Unallocated fees are never spread
heuristically.
