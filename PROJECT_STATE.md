# Mirenelle Ops - Project State

Last updated: 2026-06-21

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
- Product sets/bundles use explicit operator-confirmed recipes. A sold Amazon
  bundle SKU can consume multiple component SKU/EAN lots through FIFO.

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
  support. The limiter is shared across Orders, Returns, FBA Inventory,
  Storage Fees, and Reimbursements syncs so concurrent sync types cannot each
  consume the same quota independently. Amazon report status `FATAL` is a
  report-generation failure, not an HTTP rate-limit response.
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
3. Data Quality now includes explicit Payments-to-Orders reconciliation by
   Amazon Order ID + SKU. It reports matched/unmatched order groups and units,
   while refunds and return fees are shown separately as pending dedicated
   reconciliation.
4. Product Profitability now creates rows only from actual order products.
   Product-attributable refunds are attached only to a SKU sold in the selected
   period. Transfers, storage/service/FBA fees, and unmapped return fees remain
   in Amazon P&L instead of appearing as fake products.
5. Settings now include configurable EUR-per-unit fulfillment tariffs for FBA
   prep/storage and FBM prep, packaging, outbound logistics, and storage.
   Product Profitability shows these separately as operational costs and
   subtracts them from net profit. Storage is currently an estimated allocation
   per sold unit pending warehouse-day inventory snapshots.
6. Added FIFO inventory lots backed by purchase invoice lines. Existing
   invoice-based product costs were backfilled into 26 dated lots / 630 units.
   Product Profitability now consumes historical sales chronologically and uses
   the oldest available landed unit cost instead of the latest invoice price.
   If a product has insufficient dated lots, COGS stays missing rather than
   borrowing a future price.
7. Inventory now has operator-managed Opening Inventory Lots for stock that
   predates imported invoices. Each opening lot stores Amazon SKU, date,
   quantity, landed unit cost, currency, EAN, and notes; it participates in
   FIFO and purchased inventory quantities immediately.
8. Added official ECB daily FX sync for SEK, GBP, and PLN. Transaction reports
   and Product Profitability now convert each transaction using its own date;
   weekends and holidays use the latest prior ECB business-day rate. FIFO lots
   use the rate on the lot purchase date. Backfilled 354 ECB rows for
   2026-01-01 through 2026-06-19.
9. Rebuilt Product Costs as a complete FIFO lot registry. It now shows all 26
   lots rather than only 24 latest SKU prices, including repeated purchases,
   quantities, base cost, inbound shipping per unit, landed cost, supplier,
   source, and invoice number. Editing a cost also updates its FIFO lot.
10. Inventory now supports Bundle Recipes mapping a sold Amazon bundle SKU to
    component SKU/EAN quantities. FIFO consumes recipe components atomically
    and calculates bundle COGS from the component lots. A 12-component mask
    recipe test produced EUR 33.56 COGS for four sold bundles; test recipes
    were removed afterward.
11. Rebuilt the Bundle Recipes UI as a draft-based recipe builder:
    - bundle suggestions come from positive-quantity Amazon Orders rows, not
      Payments fee/service rows;
    - suggestions appear only after typing at least two characters and show at
      most eight results;
    - `Add component` adds or updates a component only in the browser draft;
    - multiple components can be assembled before any database write;
    - `Save bundle` atomically replaces the complete stored recipe through
      `POST /inventory/bundle-recipes`;
    - selecting an existing recipe loads it into the same editor for update;
    - the editor shows component count, total units per bundle, and estimated
      cost from the latest known component lots.
    A two-component API/UI save test passed and all temporary recipes were
    deleted afterward. The database currently contains zero confirmed real
    bundle recipes.
12. Added one shared sellable-order policy for Product Profitability, FIFO
    consumption, and Inventory sold quantities. It excludes `NON_AMAZON`,
    cancelled/canceled items, and zero-quantity rows while preserving all
    imported rows in raw/order operational views. The live database currently
    has 102 order/SKU keys: 93 eligible and 9 excluded. Four unit tests and
    live profitability/inventory endpoint checks pass.
13. After validation, run the connector for later periods and make Orders the
   source of truth for inventory sold quantities.
14. Added dedicated refund and return-fee reconciliation in Data Quality.
    Refunds match only by exact Amazon Order ID + real product SKU and validate
    refunded units against known sold units. Return-fee rows carry Amazon
    technical `X00...` SKUs, so they link to a product only when the same order
    has exactly one refunded product SKU; multiple candidates are reported as
    ambiguous rather than guessed. Imported the missing EU Orders period for
    2026-04-01 through 2026-05-04 as imports 5 and 6: 26 rows / 44 FBA units /
    1 FBM unit, with the second May chunk correctly producing zero rows.
    Orders coverage now starts on 2026-04-03. This resolved all three previously
    unmatched May refunds: 6 of 6 refund groups now match exactly.
15. Added the official FBA Customer Returns report importer
    (`GET_FBA_FULFILLMENT_CUSTOMER_RETURNS_DATA`) with migration
    `20260621_0018`, read-only SP-API sync/list endpoints, parser, deduplicated
    return items, and Amazon Connector UI controls. Imported 18 real return
    rows for 2026-04-01 through 2026-05-31. The report's FNSKU exactly matches
    the technical `X00...` SKU in Payments, so all return fees now resolve:
    6 of 6 refunds and 5 of 5 return fees match with zero ambiguous/unmatched
    groups. Matched return fees are also attributed to the correct product row
    in Product Profitability. Ten unit tests pass across order filtering,
    refund reconciliation, and returns parsing.
16. Added read-only FBA inventory snapshots from
    `GET_FBA_MYI_UNSUPPRESSED_INVENTORY_DATA` with migration
    `20260621_0019`, a connector UI action, snapshot storage, and automatic
    update of FBA Inventory rows. The first live snapshot stored 28 SKUs:
    55 fulfillable, 1 reserved, and 186 inbound units. Available stock equals
    Amazon fulfillable quantity; reserved and inbound remain separate, and
    unsellable stock is preserved in snapshot data but not counted as
    available. If Amazon rejects an immediately repeated current-state report,
    sync safely reuses the latest successful DONE report.
17. Added reimbursements ingestion from `GET_FBA_REIMBURSEMENTS_DATA`
    with migration `20260621_0020` and exact reimbursement-ID upserts. The
    first live import found one CustomerReturn reimbursement: exact
    order/SKU/FNSKU/ASIN linkage, EUR 93.84 cash, and one reimbursed unit.
    This amount is not present in Payments.
18. Added reimbursements as a separate column and KPI in Product Profitability
    and Amazon P&L. They use approval-date FX and increase Amazon operating
    result, but do not change sales, VAT, units, average selling price, gross
    profit, or FIFO COGS. EUR 93.84 appears in all-time and April 2026, and
    EUR 0 in May 2026. Product-level net remains unknown when FIFO COGS is
    incomplete; the known reimbursement remains visible separately.
19. Added detailed monthly FBA storage fees from
    `GET_FBA_STORAGE_FEE_CHARGES_DATA` with migration `20260621_0021`,
    exact FNSKU-to-SKU mapping through FBA snapshots, idempotent monthly
    upserts, and an Amazon Connector sync action. The May 2026 import contains
    87 fully mapped rows totaling EUR 5.34. For a single-month profitability
    period, actual SKU-level storage replaces the per-sold-unit estimate. May
    sold-product allocation is EUR 3.09; fees for SKUs without a product row
    stay unallocated instead of being spread heuristically.
20. Probed
    `GET_FBA_FULFILLMENT_LONGTERM_STORAGE_FEE_CHARGES_DATA`; Amazon completed
    the request as `CANCELLED`, so no empty aged-storage subsystem was added.
    Monthly storage remains the authoritative available fee source.
21. Confirmed and saved the real `Missha12-FBA-01` recipe with 12 distinct
    mask components at one unit each. May profitability matches it to four
    sold bundles, EUR 8.39 unit cost, and EUR 33.56 FIFO COGS.
22. Inventory now expands bundle sales into component movements. The four sold
    `Missha12-FBA-01` units changed every mask component from purchased 20 /
    sold 0 / on hand 20 to purchased 20 / sold 4 / on hand 16.
23. Added Bundle Assemblies with migration `20260621_0022`. Operators can
    record the date and quantity of physical bundle assembly. Each operation
    preserves a recipe snapshot, validates component availability, updates
    inventory immediately, and can be deleted to reverse the movement.
    Assemblies cover already sold bundle quantities instead of double-counting
    them. No historical assembly operations were invented; the live table is
    currently empty.
24. Added bundle assembly pricing with migration `20260621_0023`. Every
    assembly can now record who assembled it (`unknown`, prep center, Amazon,
    in-house, or other), cost per finished bundle, and currency. Product
    Profitability allocates this as a separate operational cost using FIFO
    assembly batches and the assembly-date FX rate. A live temporary check at
    EUR 0.50 reduced `Missha12-FBA-01` net profit from EUR 3.35 to EUR 2.85;
    the temporary assembly was deleted afterward. The live assemblies table
    remains empty.
25. Confirmed the business source of bundle assembly fees: the prep center
    charges them. New assembly records therefore default to `prep_center`;
    Amazon remains an explicit alternative only for exceptional cases.
26. Added in-place editing for saved assembly date, provider, unit cost,
    currency, and notes. Quantity is deliberately locked during editing because
    it represents a physical inventory movement; an incorrect quantity must be
    deleted and recorded again. Profitability picks up metadata/cost changes on
    the next report refresh. The API create/update/delete roundtrip and browser
    Edit/Cancel flow were verified; all 26 unit tests pass and the temporary
    assembly record was deleted.

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

## Current Resume Point

- Latest verified commit: `ff7877b` (`Edit bundle assembly costs`).
- Working tree was clean after the commit.
- Database migration head: `20260621_0024`.
- Bundle assembly fees are charged by the prep center and default to
  `prep_center`.
- Assembly cost is allocated to sold bundles as a separate operational cost
  using FIFO assembly batches and the FX rate on the assembly date.
- Saved assembly date, provider, unit cost, currency, and notes are editable.
  Quantity remains immutable; delete and recreate an incorrect physical
  movement.
- `Missha12-FBA-01` has a confirmed 12-component recipe. The assemblies table
  is empty because no real assembly dates, quantities, or prep-center tariff
  have been entered.
- Last verification: 26 unit tests passed; API create/update/delete and browser
    Edit/Cancel flows passed; all temporary records were removed.
27. Fixed Product Profitability to include refund-only products when an exact
    historical Amazon Order ID + SKU match exists. Prior-period refunds now
    create a real product row with zero period sales/COGS while refund amounts,
    promotional adjustments, and linked fees affect period net profit.
    Unmatched technical return-fee SKUs remain excluded. Live May verification
    now shows 12 products instead of 11; `4H-BZM0-7HOS` appears with zero
    period sales, one refund, and EUR -40.49 net profit. Total matched net
    profit changed from EUR 203.80 to EUR 163.31. All 29 tests pass.

## Current Resume Checklist

Start here:

1. Ask the operator for the real prep-center assembly tariff, currency, dates,
   and quantities for `Missha12-FBA-01`, then enter those assembly operations.
2. Refresh Product Profitability for the sales period and verify the separate
   `Bundle assembly` cost and recalculated net profit.
3. Configure confirmed real bundle recipes for the remaining bundle SKUs.
   `Missha12-FBA-01` is complete; other recipes remain business-data blockers
   because component composition needs operator input.
4. When the operator can confirm real bundle composition, open
   `http://localhost:8010/ui/`, go to `Inventory -> Bundle Recipes`, and
   enter the first confirmed real recipe:
   choose/type the sold Amazon bundle SKU, add every component SKU/EAN and its
   quantity with `Add component`, review the full draft, then click
   `Save bundle`.
5. Re-open the saved recipe from the left-hand card list and verify its
   components, total units, and estimated cost.
6. Refresh Product Profitability for the bundle's sales period and verify that
   FIFO COGS is populated from component lots.
7. Repeat for the remaining real bundle SKUs. Do not invent recipes from
   product titles; they require operator confirmation.

Useful commands:

```bash
cd /Users/pilotrw/GITHUB/mirenelle-ops
docker compose up -d
docker compose exec -T app alembic current
git status --short
```

Expected database migration head:

```text
20260621_0024
```

## Next Plan

1. Configure confirmed real bundle recipes for the remaining bundle SKUs.
2. Enter real historical/current Bundle Assembly operations when the operator
   confirms assembly dates, quantities, currency, and prep-center price per
   bundle. Do not infer quantities solely from an FBA stock snapshot.
3. Revisit aged-inventory storage only when Amazon provides a completed report;
   the current live request was cancelled.
4. Replace estimated per-sold-unit storage with warehouse-day allocation after
   inventory snapshots are available.
5. Split inventory planning by FBA/FBM logic:
   FBA uses Amazon fulfillment/inventory data; FBM needs own/prep-center stock
   and external handling tariffs.
6. Add OCR/repair fallback for image-based or malformed PDFs.
7. Later: add landed-cost model refinements for freight, prep-center costs,
   marketplace service fees, and optional allocation methods per cost type.
