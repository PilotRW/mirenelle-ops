# Mirenelle Ops - Project State

Last updated: 2026-06-07

## Product Direction

Create a separate service for ecommerce operations and accounting:

- inventory/accounting;
- supplier purchases;
- Amazon sales/imports;
- cashflow;
- stock forecasting;
- replenishment recommendations;
- future integration with `oa-pipeline`.

## Architecture Decisions

- Keep this project separate from `oa-pipeline`.
- Use a separate database: `mirenelle_ops`.
- It may run against the same local Postgres instance as `oa-pipeline`.
- Do not mix Alembic migrations or application tables with the `oa` database.
- Integrate with `oa-pipeline` later through API/export boundaries.
- Start with report ingestion; add Amazon SP-API only as a read-only/download
  connector.
- Marketplace reports stay in the original sale currency.
- General/consolidated reports are shown in EUR.
- Amazon API integration must not push/write data to Amazon.
- Supplier invoice inbound shipping is treated as landed cost. Default
  allocation is by purchased unit quantity, with an alternative by line value.
- Product sets/bundles are deferred because current sold sets are represented
  as single sellable products, not assembled from component inventory.

## Current Input Reports

Known first inputs:

1. Amazon Payments Transaction View per marketplace.
2. Customer Returns.
3. Reimbursements.
4. Service Fees.
5. Product cost catalog with `Nazwa produktu / SKU / Zakup EUR`.

Initial inspected transaction reports:

- Belgium: English headers, EUR.
- Spain: English headers, EUR.
- Netherlands: English headers, EUR.
- Sweden: English headers, SEK.
- Germany: German headers, EUR.

Observed German transaction types:

- `Bezahlung der Bestellung`
- `Service-Gebühren`
- `Erstattung`

## Locale Mapping Policy

Header mapping must be locale-safe:

- support expected European Amazon languages;
- block commit if required columns are missing;
- block commit if a header maps ambiguously;
- show detected mapping in preview;
- allow operator-confirmed manual mapping later;
- save reusable mapping profiles later.

Initial target languages:

- English
- German
- French
- Italian
- Spanish
- Dutch
- Polish
- Swedish

## Next Steps

Completed:

- Created project skeleton.
- Created separate `mirenelle_ops` database in the existing local Postgres.
- Added and applied initial Alembic migration.
- Added Amazon Payments Transaction View preview endpoint:
  `POST /imports/amazon-payments/preview`.
- Added Amazon Payments commit endpoint:
  `POST /imports/amazon-payments/commit`.
- Added SHA-256 duplicate import protection.
- Added product cost catalog preview/commit endpoints.
- Added monthly cashflow and latest product cost reports.
- Added a lightweight local operator UI at `/ui/`.
- General cashflow now includes EUR-converted totals while marketplace rows
  keep original sale currency.
- Added operator-configurable FX rates in the database and UI.
- Added generic preview endpoint/UI for Customer Returns, Reimbursements, and
  Service Fees report shape discovery.
- Added raw generic report commit/list endpoints for those upcoming report
  types.
- Added mock cost generation from current transactions.
- Added product profitability analytics using mocked/known costs.
- Added English/German/Ukrainian UI translations using the same `data-i18n`
  pattern as `oa-pipeline`.
- Added purchase invoice importer for CSV/XLSX invoices.
- Purchase invoices now create `purchase_invoices`,
  `purchase_invoice_lines`, and linked `product_costs` rows.
- Added text-based PDF invoice preview/import via `pypdf`, including
  supplier/invoice metadata and EU-style line extraction for product, EAN,
  quantity, VAT, unit cost, and totals.
- Added invoice line classification. Product lines are separated from inbound
  shipping, fulfillment fees, marketplace fees, and service/other expense lines.
  Only product lines create `product_costs`.
- Added purchase summary report.
- Verified sample invoice import updates product profitability from invoice
  unit costs.
- Added product mapping suggestions/confirmation so invoice lines can be
  connected to Amazon transaction product names.
- Product profitability now uses confirmed product mappings before marking a
  product as missing cost.
- Added dashboard period filtering. Monthly cashflow, product profitability,
  purchase summary, and dashboard KPI tiles now accept/use `start_date` and
  `end_date`.
- Verified preview with German and Swedish transaction files.
- Committed sample transaction files for DE, BE, ES, NL, and SE into the local
  `mirenelle_ops` database.
- Added landed-cost allocation settings and applied default quantity-based
  inbound shipping allocation into product costs.
- Added inventory sync that matches invoice purchases to Amazon sales by SKU,
  confirmed mappings, aliases, and fuzzy product names.
- Inventory now shows purchased quantity, sold quantity, and on-hand quantity.
- Fixed Amazon Payments quantity handling for multi-unit order rows.
- Added fulfillment channel parsing for Amazon Payments. Imported payment lines
  now preserve FBA/FBM/UNKNOWN, payment line details display fulfillment, and
  profitability/P&L can split rows by fulfillment channel.
- Added read-only Amazon SP-API Orders connector scaffold: status endpoint,
  manual All Orders report preview/commit, imports list, order import tables,
  and report parser for FBA/FBM quantities.

Current verified inventory examples:

- `I2318`: purchased 121, sold 19, on hand 102.
- `I8510`: purchased 70, sold 19, on hand 51.
- `L1006`: purchased 10, sold 9, on hand 1.
- `Dr.Beckmann`: purchased 24, sold 13, on hand 11.
- `Cif`: purchased 32, sold 4, on hand 28.

Next:

1. Implement the real read-only SP-API report download worker:
   `createReport` -> poll `getReport` -> `getReportDocument` -> download ->
   import through the existing parser.
2. Use imported Amazon Orders as the source of truth for order quantity,
   fulfillment channel, SKU, and ASIN; keep Amazon Payments as the money/fees
   source and reconcile by order/SKU/period.
3. Add Fulfillment-Box / prep-center tariff settings for storage, prep,
   labels, packing, and outbound handling.
4. Add read-only FBA inventory connector after SP-API credentials are available.
5. Add Customer Returns import after seeing the real file headers.
6. Add Reimbursements import after seeing the real file headers.
7. Add Service Fees import if the separate report has richer fields than
   Transaction View.
8. Add OCR/repair fallback for image-based or malformed PDFs.
