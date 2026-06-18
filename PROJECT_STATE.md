# Mirenelle Ops - Project State

Last updated: 2026-06-18

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
- Purchase invoice product costs are net of input VAT. Invoice VAT is stored
  separately for cash/accounting visibility and must not inflate COGS.
- Amazon Payments `product_charges` are treated as net sales excluding VAT.
  Live order/payment reconciliation showed that Orders item price minus item
  tax closely matches Payments product charges. Product profitability therefore
  uses Payments charges as net revenue, Orders tax as sales VAT, and net plus
  VAT as gross revenue. Profit/margin/ROI are calculated from net revenue.
- SP-API production access requires an approved Amazon Developer Profile. The
  project now has `SECURITY_INCIDENT_RESPONSE.md` to document the required
  incident response roles, 6-month review cycle, 24-hour notification process,
  and Amazon notification at `security@amazon.com`.
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
- Added the first real read-only SP-API Orders download worker. The UI now has
  a visible `Amazon Connector` page that can request
  `GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_GENERAL`, poll processing,
  download the report document, and import it through the existing order parser.
  Periods longer than 30 days are split into multiple report requests.
- Amazon Connector defaults to `All EU marketplaces` because the account can
  sell across Europe even when Germany is the primary marketplace. The current
  EU set is DE, FR, IT, ES, NL, BE, PL, and SE.
- Amazon Connector has conservative Reports API rate-limit protection:
  `createReport` is spaced at least 65 seconds apart across the whole sync run,
  and retryable Amazon responses are retried with backoff and `Retry-After`
  support.
- Dashboard and Product Profitability now include sellerboard-style operating
  metrics from existing data: sales, orders/units, refunds, Amazon fees,
  gross profit, net profit, margins, ROI, and product status counts. Ads, BSR,
  and forecast remain future integrations because current inputs do not provide
  those values.
- Purchase Invoices now show VAT status/amounts so operators can distinguish
  invoices with VAT from invoices without VAT.
- Product Profitability now exposes gross revenue, sales VAT, and net revenue.
  The API fields are `revenue_gross_eur`, `sales_vat_eur`, and `revenue_eur`;
  the UI shows them as separate columns. Net revenue is used for gross profit,
  net profit, margin, and ROI.
- Added `SECURITY_INCIDENT_RESPONSE.md` to support corrected Amazon Developer
  Profile responses for incident response requirements.
- Submitted an Amazon Solution Provider Portal support case under Access
  issues to request Developer Profile resubmission/reassessment after adopting
  the incident response plan. Amazon reopened the registration flow, and the
  corrected Developer Profile was subsequently approved.
- Amazon approved the SP-API Developer Profile and granted global marketplace
  access for the requested roles.
- Registered and self-authorized the private production `Mirenelle Ops`
  application for the seller account. LWA Client ID, Client Secret, and refresh
  token are stored only in the ignored local `.env`.
- Verified the production connector without exposing credentials: LWA token
  exchange returned `AUTH_OK`, and the read-only Reports API `getReports`
  request for the All Orders report type returned `REPORTS_API_OK`.
- Ran the first live All Orders downloads:
  - DE, 2026-05-01 through 2026-05-03: report completed successfully with zero
    rows.
  - DE, 2026-05-15: report completed successfully and was stored as order
    import with 7 rows, 7 orders, 6 shipped FBA units, 1 cancelled zero-quantity
    row, SKU/ASIN coverage on all rows, and real item tax values.
  - These two test import records were later superseded by the full EU snapshot
    and removed after their rows were safely upserted.
- The 2026-05-15 report included both `Amazon.de` EUR rows and one `Amazon.se`
  SEK row even though the report request used the DE marketplace ID. This
  proved that marketplace must be derived per row from `sales-channel`.
- Updated the order parser to map `Amazon.de`, `Amazon.se`, and the other
  supported EU sales channels to the correct marketplace code.
- Updated All EU sync to create one report request containing all eight EU
  marketplace IDs instead of making eight report requests that could return
  overlapping order data.
- Fixed sales VAT aggregation so a cancelled order row with a null currency
  cannot overwrite non-zero VAT for the same SKU/fulfillment/currency key.
- Verified VAT-aware profitability for 2026-05-15:
  Payments product charges match Orders item price less item tax, proving that
  Payments charges are already net and VAT must not be subtracted again.
- Added overlap-safe order upserts with a global unique key on Amazon Order ID,
  SKU, and ASIN. Re-importing an overlapping period updates the existing item
  instead of duplicating it.
- Downloaded the full EU All Orders report for 2026-05-01 through 2026-05-30:
  99 unique rows, 97 orders, and 105 units. The overlap with the previous
  one-day test remained 99 unique rows, confirming dedupe works.
- Exact Payments-to-Orders reconciliation by Amazon Order ID + SKU matched
  78 of 78 order/SKU groups, with 84 Payments units equal to 84 Orders units.
- Added Amazon Ireland (`Amazon.ie`, marketplace ID `A28R8C7NBKEWEA`) to the
  EU connector. `Non-Amazon` fulfillment rows are classified separately as
  `NON_AMAZON` and must not be counted as marketplace sales.

## Current Resume Point

The SP-API production connector, overlap-safe imports, and exact order/SKU
reconciliation are operational. Continue from this point:

1. Exact Orders metadata is now applied inside Product Profitability:
   quantity, ASIN, fulfillment channel, marketplace, and sales VAT come from
   the matched order; product charges, refunds, promotions, Amazon fees, and
   settlement dates come from Payments.
2. Corrected VAT output is verified for May 2026:
   `revenue_eur` EUR 1,456.87 is net Payments charges,
   `sales_vat_eur` EUR 286.60 is Orders tax, and
   `revenue_gross_eur` EUR 1,743.47 is net plus VAT.
3. Add an explicit reconciliation/data-quality report showing matched and
   unmatched order/SKU groups. Current order transactions match 78/78; unmatched
   payment rows are refunds and return-fee rows, which require separate refund
   reconciliation.
4. Exclude `NON_AMAZON` fulfillment rows and cancelled zero-quantity rows from
   sold-unit analytics. Preserve them in raw/order operational views.
5. After validation, run the connector for later periods and make Orders the
   source of truth for inventory sold quantities.

Operational notes:

- `.env` contains production credentials locally and is ignored by Git. Never
  print, commit, paste, or screenshot its values.
- `getMarketplaceParticipations` returned HTTP 403 because the app does not
  have a Sellers API role. This is not a connector failure; the required
  Reports API is authorized and works.
- The live app is available at `http://localhost:8010/ui/`.
- The current order imports endpoint is
  `GET /integrations/amazon-sp-api/orders/imports`.
- The live sync endpoint is
  `POST /integrations/amazon-sp-api/orders/sync`.

Current verified inventory examples:

- `I2318`: purchased 121, sold 19, on hand 102.
- `I8510`: purchased 70, sold 19, on hand 51.
- `L1006`: purchased 10, sold 9, on hand 1.
- `Dr.Beckmann`: purchased 24, sold 13, on hand 11.
- `Cif`: purchased 32, sold 4, on hand 28.

Next Plan:

1. Add reconciliation coverage and unmatched-row diagnostics to Data Quality.
2. Implement separate refund/return-fee reconciliation; these rows do not
   currently match the sales order ID directly.
3. Add Fulfillment-Box / prep-center tariff settings for storage, prep,
   labels, packing, and outbound handling.
4. Split profitability and inventory planning by FBA/FBM logic:
   FBA uses Amazon fulfillment/inventory data; FBM needs own/prep-center stock
   and external handling tariffs.
5. Add read-only FBA inventory connector.
6. Add Customer Returns import after seeing the real file headers.
7. Add Reimbursements import after seeing the real file headers.
8. Add Service Fees import if the separate report has richer fields than
   Transaction View.
9. Add OCR/repair fallback for image-based or malformed PDFs.
10. Later: add landed-cost model refinements for freight, prep-center costs,
    marketplace service fees, and optional allocation methods per cost type.
