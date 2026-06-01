# Mirenelle Ops - Project State

Last updated: 2026-05-29

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
- Start with report ingestion before Amazon API/SP-API connectors.
- Marketplace reports stay in the original sale currency.
- General/consolidated reports are shown in EUR.

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

Next:

1. Test purchase invoice importer with more real supplier invoice layouts.
2. Return to landed-cost allocation after several real invoice imports and
   expense taxonomy stabilization. Initial default should likely allocate
   inbound shipping by product subtotal, with quantity/manual alternatives.
3. Test with the remaining marketplace transaction reports.
4. Add OCR/repair fallback for image-based or malformed PDFs.
5. Add manual edit/search flow for product mappings beyond suggested matches.
6. Add Customer Returns import after seeing the real file headers.
7. Add Reimbursements import after seeing the real file headers.
8. Add Service Fees import if the separate report has richer fields than
   Transaction View.
