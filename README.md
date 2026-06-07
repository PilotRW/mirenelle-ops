# Mirenelle Ops

Operations, accounting, inventory, and forecasting service for Mirenelle.

This project is separate from `oa-pipeline`. OA Pipeline finds supplier and
Amazon deal candidates; Mirenelle Ops tracks what happened operationally:
Amazon transactions, product costs, inventory movements, cashflow, stock
forecasting, and replenishment recommendations.

## Current Scope

Initial MVP:

- Import Amazon Payments Transaction View CSV files.
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
```

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

Manual All Orders report upload remains available on the same page as a
fallback/debug path.
