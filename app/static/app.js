const translations = {
  en: {
    "app.tagline": "Amazon accounting imports, product costs, and monthly cashflow.",
    "action.add": "Add",
    "action.addOpeningLot": "Add opening lot",
    "action.addComponent": "Add component",
    "action.saveBundle": "Save bundle",
    "action.commit": "Commit",
    "action.commitRaw": "Commit raw",
    "action.mockCosts": "Mock Costs",
    "action.preview": "Preview",
    "action.refresh": "Refresh",
    "action.refreshReports": "Refresh reports",
    "action.search": "Search",
    "action.save": "Save",
    "action.cancel": "Cancel",
    "action.clear": "Clear",
    "action.edit": "Edit",
    "action.delete": "Delete",
    "action.manualStockEntry": "Manual stock entry",
    "action.downloadOrders": "Download orders",
    "action.downloadReturns": "Download customer returns",
    "action.commitManualReport": "Commit manual report",
    "action.syncOaCatalog": "Sync OA catalog",
    "action.syncInventory": "Sync stock",
    "action.syncFbaInventory": "Sync FBA inventory",
    "action.syncEcbRates": "Sync ECB rates",
    "action.useMatch": "Use",
    "action.viewLines": "Lines",
    "allocation.byLineValue": "By line value",
    "allocation.byQuantity": "By quantity",
    "field.allocationMethod": "Allocation method",
    "field.costFile": "Cost CSV/XLSX",
    "field.csvReport": "CSV report",
    "field.currency": "Currency",
    "field.effectiveDate": "Effective date",
    "field.endDate": "End date",
    "field.invoiceDate": "Invoice date",
    "field.invoiceNumber": "Invoice",
    "field.invoiceFile": "Invoice CSV/XLSX/PDF",
    "field.invoiceNumber": "Invoice number",
    "field.marketplace": "Marketplace",
    "field.ordersReport": "All Orders report",
    "field.rateToEur": "Rate to EUR",
    "field.reportType": "Report type",
    "field.search": "Search",
    "field.startDate": "Start date",
    "field.supplier": "Supplier",
    "field.supplierSku": "Supplier SKU",
    "field.productName": "Product name",
    "field.fulfillment": "Fulfillment",
    "field.bundleSku": "Bundle Amazon SKU",
    "field.bundleName": "Bundle name",
    "field.componentSku": "Component SKU / EAN",
    "field.componentQuantity": "Component quantity",
    "field.fbaPrepPerUnit": "FBA prep / unit EUR",
    "field.fbaStoragePerUnit": "FBA storage / sold unit EUR",
    "field.fbmPrepPerUnit": "FBM prep / unit EUR",
    "field.fbmPackagingPerUnit": "FBM packaging / unit EUR",
    "field.fbmOutboundPerUnit": "FBM outbound / unit EUR",
    "field.fbmStoragePerUnit": "FBM storage / sold unit EUR",
    "field.amazonProductSearch": "Amazon product search",
    "field.invoiceProductSearch": "Invoice product search",
    "field.invoiceProductsSearch": "Invoice product search",
    "field.transactionCsv": "Transaction CSV",
    "message.committedRaw": "Committed raw report.",
    "message.noData": "No data",
    "message.noPreview": "No preview loaded.",
    "message.confirmDeletePayment": "Delete this Amazon Payments report? This will remove its transactions from analytics.",
    "message.confirmDeleteInvoice": "Delete this purchase invoice? Its invoice lines, invoice product costs, and mappings will be removed.",
    "message.confirmDeleteCostImport": "Delete this product cost import? Its product costs will be removed from analytics.",
    "message.confirmDeleteGenericReport": "Delete this raw report import?",
    "message.confirmDeleteInventory": "Delete this inventory item?",
    "message.confirmDeleteOpeningLot": "Delete this opening inventory lot?",
    "message.confirmDeleteComponent": "Delete this bundle component?",
    "recipe.chooseBundle": "Choose a bundle or start a new recipe",
    "recipe.componentLines": "Components",
    "recipe.totalUnits": "Units per bundle",
    "recipe.estimatedCost": "Estimated recipe cost",
    "recipe.empty": "No components yet. Add the first product above.",
    "recipe.purchased": "Purchased in FIFO lots",
    "recipe.latestCost": "Latest lot cost",
    "recipe.unsaved": "Unsaved changes",
    "message.selectInvoiceLine": "Select an invoice product first.",
    "message.storageAllocationNote": "Storage is currently estimated per sold unit until warehouse-day inventory snapshots are available.",
    "marketplace.eu": "All EU marketplaces",
    "metric.withEan": "With EAN",
    "preview.detectedFields": "Detected fields",
    "preview.expenses": "Expenses",
    "preview.invoice": "Invoice",
    "preview.lines": "Lines",
    "preview.noIssues": "No issues detected.",
    "preview.needsReview": "Needs review",
    "preview.previewReady": "Preview ready",
    "preview.quantity": "Quantity",
    "preview.subtotal": "Subtotal",
    "preview.products": "Products",
    "preview.total": "Total",
    "preview.unknownHeaders": "Unknown headers",
    "preview.validationErrors": "Validation errors",
    "nav.dashboard": "Dashboard",
    "nav.imports": "Imports",
    "nav.operations": "Operations",
    "nav.overview": "Overview",
    "nav.settings": "Settings",
    "period.all": "All time",
    "period.custom": "Custom",
    "period.lastMonth": "Last month",
    "period.thisMonth": "This month",
    "paymentCategory.fbaFee": "FBA fee",
    "paymentCategory.order": "Order",
    "paymentCategory.other": "Other",
    "paymentCategory.refund": "Refund",
    "paymentCategory.returnFee": "Return fee",
    "paymentCategory.serviceFee": "Service fee",
    "paymentCategory.transfer": "Transfer",
    "paymentCategory.unknown": "Unknown",
    "report.customerReturns": "Customer Returns",
    "report.reimbursements": "Reimbursements",
    "report.serviceFees": "Service Fees",
    "section.amazonPayments": "Amazon Payments",
    "section.amazonConnector": "Amazon SP-API",
    "section.fxRates": "FX Rates",
    "section.generalCashflow": "General Cashflow",
    "section.inventory": "Inventory",
    "section.openingInventoryLots": "Opening Inventory Lots",
    "section.bundleRecipes": "Bundle Recipes",
    "section.invoiceLines": "Invoice Lines",
    "section.landedCost": "Landed Cost",
    "section.fulfillmentCosts": "Fulfillment Costs",
    "section.paymentLines": "Payment Lines",
    "section.productCosts": "Product Costs",
    "section.productMappings": "Product Mappings",
    "section.oaCatalog": "OA Catalog",
    "section.amazonPnl": "Amazon P&L",
    "section.dataQuality": "Data Quality",
    "section.reconciliation": "Payments / Orders reconciliation",
    "section.missingCosts": "Missing product costs",
    "section.productProfitability": "Product Profitability",
    "section.purchaseSummary": "Purchase Summary",
    "section.purchaseInvoices": "Purchase Invoices",
    "section.reportPreview": "Report Preview",
    "status.committed": "Committed",
    "status.duplicate": "Already imported",
    "status.imported": "Imported",
    "status.loaded": "Loaded",
    "status.loading": "Loading",
    "status.mockCostsCreated": "Mock costs created",
    "status.mockingCosts": "Mocking costs",
    "status.matched": "matched",
    "status.missingCost": "missing cost",
    "status.profitable": "profitable",
    "status.loss": "loss",
    "status.breakeven": "breakeven",
    "status.unknown": "unknown",
    "status.unmapped": "unmapped",
    "status.unmatched": "unmatched",
    "status.quantityMismatch": "quantity mismatch",
    "status.ambiguous": "ambiguous",
    "status.refundPending": "refund: separate reconciliation",
    "status.returnFeePending": "return fee: separate reconciliation",
    "status.healthy": "healthy",
    "status.lowStock": "low stock",
    "status.outOfStock": "out of stock",
    "status.ready": "Ready",
    "status.saved": "Saved",
    "status.saving": "Saving",
    "status.uploading": "Uploading",
    "vat.included": "VAT included",
    "vat.none": "No VAT",
    "vat.unknown": "VAT unknown",
    "table.action": "Action",
    "table.amazonProduct": "Amazon product",
    "table.amazonFees": "Amazon fees",
    "table.avgSellingPrice": "Avg selling price",
    "table.amazonOperatingResult": "Amazon operating result",
    "table.baseCost": "Base cost",
    "table.cogsEur": "COGS EUR",
    "table.confidence": "Confidence",
    "table.cost": "Cost",
    "table.costCoverage": "Cost coverage",
    "table.costEur": "Cost EUR",
    "table.date": "Date",
    "table.effective": "Effective",
    "table.estPayout": "Est. payout",
    "table.expenseCategory": "Expense category",
    "table.fees": "Fees",
    "table.file": "File",
    "table.fxToEur": "FX to EUR",
    "table.generalTotalEur": "General total in EUR",
    "table.grossSales": "Gross sales",
    "table.grossProfit": "Gross Profit",
    "table.id": "ID",
    "table.identifiers": "ASIN / SKU / EAN",
    "table.invoiceProduct": "Invoice product",
    "table.inboundShipping": "Inbound shipping",
    "table.inboundPerUnit": "Inbound / unit",
    "table.landedCost": "Landed cost",
    "table.available": "Available",
    "table.inbound": "Inbound",
    "table.lineType": "Line type",
    "table.lastSync": "Last sync",
    "table.market": "Market",
    "table.margin": "Margin",
    "table.marketplaceCurrencyTotal": "{currency} marketplace currency total",
    "table.matchedCogs": "Matched COGS",
    "table.matchedGrossProfit": "Matched gross profit",
    "table.matchedRoi": "Matched ROI",
    "table.month": "Month",
    "table.name": "Name",
    "table.netMargin": "Net margin",
    "table.netProfit": "Net profit",
    "table.netRoi": "Net ROI",
    "table.other": "Other",
    "table.operationalCosts": "Operational costs",
    "table.onHand": "On hand",
    "table.paymentRows": "Payment rows",
    "table.period": "Period",
    "table.product": "Product",
    "table.productCharges": "Product charges",
    "table.promo": "Promo",
    "table.purchased": "Purchased",
    "table.refunds": "Refunds",
    "table.reorderPoint": "Reorder point",
    "table.reserved": "Reserved",
    "table.quantity": "Quantity",
    "table.revenueEur": "Revenue EUR",
    "table.revenueGrossEur": "Revenue gross EUR",
    "table.revenueNetEur": "Revenue net EUR",
    "table.revenue": "Revenue",
    "table.roi": "ROI",
    "table.rows": "Rows",
    "table.ordersUnits": "Orders / Units",
    "table.orderId": "Order ID",
    "table.orderMatch": "Order match",
    "table.orderUnits": "Order units",
    "table.paymentUnits": "Payment units",
    "table.refundGroups": "Refund groups",
    "table.refundMatch": "Refund match",
    "table.returnFeeMatch": "Return fee match",
    "table.linkedSku": "Linked SKU",
    "table.sales": "Sales",
    "table.salesVat": "Sales VAT",
    "table.salesCurrency": "Sales currency",
    "table.sku": "SKU",
    "table.sold": "Sold",
    "table.source": "Source",
    "table.stockFlow": "Stock flow",
    "table.stockAlerts": "Stock alerts",
    "table.status": "Status",
    "table.subtotal": "Subtotal",
    "table.total": "Total",
    "table.totalEur": "Total EUR",
    "table.vat": "VAT",
    "table.vatAmount": "VAT amount",
    "table.vatRate": "VAT rate",
    "table.vatStatus": "VAT",
    "table.notes": "Notes",
    "table.transfers": "Transfers",
    "table.type": "Type",
    "table.units": "Units",
    "table.unitsRefunded": "Units refunded",
    "table.unitsSold": "Units sold",
    "table.unknownTypes": "Unknown types",
  },
  de: {
    "app.tagline": "Amazon-Buchhaltungsimporte, Einkaufspreise und monatlicher Cashflow.",
    "action.add": "Hinzufügen",
    "action.addOpeningLot": "Anfangsbestand hinzufügen",
    "action.addComponent": "Komponente hinzufügen",
    "action.saveBundle": "Bundle speichern",
    "action.commit": "Speichern",
    "action.commitRaw": "Rohdaten speichern",
    "action.mockCosts": "Preise mocken",
    "action.preview": "Vorschau",
    "action.refresh": "Aktualisieren",
    "action.refreshReports": "Reports aktualisieren",
    "action.search": "Suchen",
    "action.save": "Speichern",
    "action.cancel": "Abbrechen",
    "action.clear": "Leeren",
    "action.edit": "Bearbeiten",
    "action.delete": "Löschen",
    "action.manualStockEntry": "Bestand manuell erfassen",
    "action.downloadOrders": "Bestellungen laden",
    "action.downloadReturns": "Kundenrücksendungen laden",
    "action.commitManualReport": "Manuellen Report speichern",
    "action.syncOaCatalog": "OA-Katalog synchronisieren",
    "action.syncInventory": "Bestand synchronisieren",
    "action.syncFbaInventory": "FBA-Bestand synchronisieren",
    "action.syncEcbRates": "ECB-Kurse synchronisieren",
    "action.useMatch": "Nutzen",
    "action.viewLines": "Zeilen",
    "allocation.byLineValue": "Nach Zeilenwert",
    "allocation.byQuantity": "Nach Menge",
    "field.allocationMethod": "Verteilungsmethode",
    "field.costFile": "Kosten CSV/XLSX",
    "field.csvReport": "CSV-Report",
    "field.currency": "Währung",
    "field.effectiveDate": "Gültig ab",
    "field.endDate": "Enddatum",
    "field.invoiceDate": "Rechnungsdatum",
    "field.invoiceNumber": "Rechnung",
    "field.invoiceFile": "Rechnung CSV/XLSX/PDF",
    "field.invoiceNumber": "Rechnungsnummer",
    "field.marketplace": "Marketplace",
    "field.ordersReport": "All-Orders-Report",
    "field.rateToEur": "Kurs zu EUR",
    "field.reportType": "Reporttyp",
    "field.search": "Suchen",
    "field.startDate": "Startdatum",
    "field.supplier": "Lieferant",
    "field.supplierSku": "Lieferanten-SKU",
    "field.productName": "Produktname",
    "field.fulfillment": "Fulfillment",
    "field.bundleSku": "Bundle Amazon SKU",
    "field.bundleName": "Bundle-Name",
    "field.componentSku": "Komponenten-SKU / EAN",
    "field.componentQuantity": "Komponentenmenge",
    "field.fbaPrepPerUnit": "FBA Vorbereitung / Einheit EUR",
    "field.fbaStoragePerUnit": "FBA Lager / verkaufte Einheit EUR",
    "field.fbmPrepPerUnit": "FBM Vorbereitung / Einheit EUR",
    "field.fbmPackagingPerUnit": "FBM Verpackung / Einheit EUR",
    "field.fbmOutboundPerUnit": "FBM Versand / Einheit EUR",
    "field.fbmStoragePerUnit": "FBM Lager / verkaufte Einheit EUR",
    "field.amazonProductSearch": "Amazon-Produkt suchen",
    "field.invoiceProductSearch": "Rechnungsprodukt suchen",
    "field.invoiceProductsSearch": "Rechnungsprodukt suchen",
    "field.transactionCsv": "Transaktions-CSV",
    "message.committedRaw": "Rohdaten gespeichert.",
    "message.noData": "Keine Daten",
    "message.noPreview": "Keine Vorschau geladen.",
    "message.confirmDeletePayment": "Diesen Amazon-Zahlungsreport löschen? Die Transaktionen werden aus der Analyse entfernt.",
    "message.confirmDeleteInvoice": "Diese Einkaufsrechnung löschen? Rechnungszeilen, daraus erzeugte Produktkosten und Zuordnungen werden entfernt.",
    "message.confirmDeleteCostImport": "Diesen Produktkosten-Import löschen? Die Produktkosten werden aus der Analyse entfernt.",
    "message.confirmDeleteGenericReport": "Diesen Rohreport-Import löschen?",
    "message.confirmDeleteInventory": "Diesen Bestandseintrag löschen?",
    "message.confirmDeleteOpeningLot": "Diese Anfangsbestands-Charge löschen?",
    "message.confirmDeleteComponent": "Diese Bundle-Komponente löschen?",
    "recipe.chooseBundle": "Bundle wählen oder ein neues Rezept anlegen",
    "recipe.componentLines": "Komponenten",
    "recipe.totalUnits": "Einheiten pro Bundle",
    "recipe.estimatedCost": "Geschätzte Rezeptkosten",
    "recipe.empty": "Noch keine Komponenten. Fügen Sie oben das erste Produkt hinzu.",
    "recipe.purchased": "In FIFO-Losen eingekauft",
    "recipe.latestCost": "Letzter Lospreis",
    "recipe.unsaved": "Nicht gespeicherte Änderungen",
    "message.selectInvoiceLine": "Wähle zuerst ein Rechnungsprodukt.",
    "message.storageAllocationNote": "Lagerkosten werden vorerst pro verkaufter Einheit geschätzt, bis tägliche Bestands-Snapshots verfügbar sind.",
    "marketplace.eu": "Alle EU-Marketplaces",
    "metric.withEan": "Mit EAN",
    "preview.detectedFields": "Erkannte Felder",
    "preview.expenses": "Ausgaben",
    "preview.invoice": "Rechnung",
    "preview.lines": "Zeilen",
    "preview.noIssues": "Keine Probleme erkannt.",
    "preview.needsReview": "Prüfen",
    "preview.previewReady": "Vorschau bereit",
    "preview.quantity": "Menge",
    "preview.subtotal": "Zwischensumme",
    "preview.products": "Produkte",
    "preview.total": "Summe",
    "preview.unknownHeaders": "Unbekannte Spalten",
    "preview.validationErrors": "Validierungsfehler",
    "nav.dashboard": "Dashboard",
    "nav.imports": "Importe",
    "nav.operations": "Operationen",
    "nav.overview": "Übersicht",
    "nav.settings": "Einstellungen",
    "period.all": "Alle Zeit",
    "period.custom": "Benutzerdefiniert",
    "period.lastMonth": "Letzter Monat",
    "period.thisMonth": "Dieser Monat",
    "paymentCategory.fbaFee": "FBA-Gebühr",
    "paymentCategory.order": "Bestellung",
    "paymentCategory.other": "Sonstiges",
    "paymentCategory.refund": "Erstattung",
    "paymentCategory.returnFee": "Rücksendegebühr",
    "paymentCategory.serviceFee": "Servicegebühr",
    "paymentCategory.transfer": "Übertrag",
    "paymentCategory.unknown": "Unbekannt",
    "report.customerReturns": "Kundenrücksendungen",
    "report.reimbursements": "Erstattungen",
    "report.serviceFees": "Servicegebühren",
    "section.amazonPayments": "Amazon-Zahlungen",
    "section.amazonConnector": "Amazon SP-API",
    "section.fxRates": "Wechselkurse",
    "section.generalCashflow": "Gesamt-Cashflow",
    "section.inventory": "Bestand",
    "section.openingInventoryLots": "Anfangsbestands-Chargen",
    "section.bundleRecipes": "Bundle-Rezepte",
    "section.invoiceLines": "Rechnungszeilen",
    "section.landedCost": "Landed Cost",
    "section.fulfillmentCosts": "Fulfillment-Kosten",
    "section.paymentLines": "Zahlungszeilen",
    "section.productCosts": "Einkaufspreise",
    "section.productMappings": "Produktzuordnung",
    "section.oaCatalog": "OA-Katalog",
    "section.amazonPnl": "Amazon P&L",
    "section.dataQuality": "Datenqualität",
    "section.reconciliation": "Abgleich Zahlungen / Bestellungen",
    "section.missingCosts": "Fehlende Produktkosten",
    "section.productProfitability": "Produktprofitabilität",
    "section.purchaseSummary": "Einkaufsübersicht",
    "section.purchaseInvoices": "Einkaufsrechnungen",
    "section.reportPreview": "Report-Vorschau",
    "status.committed": "Gespeichert",
    "status.duplicate": "Bereits importiert",
    "status.imported": "Importiert",
    "status.loaded": "Geladen",
    "status.loading": "Lädt",
    "status.mockCostsCreated": "Mock-Preise erstellt",
    "status.mockingCosts": "Mock-Preise werden erstellt",
    "status.matched": "zugeordnet",
    "status.missingCost": "Kosten fehlen",
    "status.profitable": "profitabel",
    "status.loss": "Verlust",
    "status.breakeven": "Null",
    "status.unknown": "unbekannt",
    "status.unmapped": "nicht zugeordnet",
    "status.unmatched": "nicht zugeordnet",
    "status.quantityMismatch": "Mengenabweichung",
    "status.ambiguous": "mehrdeutig",
    "status.refundPending": "Erstattung: separater Abgleich",
    "status.returnFeePending": "Rücksendegebühr: separater Abgleich",
    "status.healthy": "gesund",
    "status.lowStock": "niedriger Bestand",
    "status.outOfStock": "ausverkauft",
    "status.ready": "Bereit",
    "status.saved": "Gespeichert",
    "status.saving": "Speichert",
    "status.uploading": "Lädt hoch",
    "vat.included": "mit MwSt.",
    "vat.none": "ohne MwSt.",
    "vat.unknown": "MwSt. unbekannt",
    "table.action": "Aktion",
    "table.amazonProduct": "Amazon-Produkt",
    "table.amazonFees": "Amazon-Gebühren",
    "table.avgSellingPrice": "Ø Verkaufspreis",
    "table.amazonOperatingResult": "Amazon-Betriebsergebnis",
    "table.baseCost": "Basispreis",
    "table.cogsEur": "Wareneinsatz EUR",
    "table.confidence": "Konfidenz",
    "table.cost": "Kosten",
    "table.costCoverage": "Kostenabdeckung",
    "table.costEur": "Kosten EUR",
    "table.date": "Datum",
    "table.effective": "Gültig",
    "table.estPayout": "Geschätzte Auszahlung",
    "table.expenseCategory": "Ausgabenkategorie",
    "table.fees": "Gebühren",
    "table.file": "Datei",
    "table.fxToEur": "Kurs zu EUR",
    "table.generalTotalEur": "Gesamtsumme in EUR",
    "table.grossSales": "Bruttoumsatz",
    "table.grossProfit": "Bruttogewinn",
    "table.id": "ID",
    "table.identifiers": "ASIN / SKU / EAN",
    "table.invoiceProduct": "Rechnungsprodukt",
    "table.available": "Verfügbar",
    "table.inbound": "Inbound",
    "table.inboundShipping": "Transport",
    "table.inboundPerUnit": "Transport / Einheit",
    "table.landedCost": "Landed Cost",
    "table.lineType": "Zeilentyp",
    "table.lastSync": "Letzte Synchronisierung",
    "table.market": "Markt",
    "table.margin": "Marge",
    "table.marketplaceCurrencyTotal": "{currency} Summe in Marktwährung",
    "table.matchedCogs": "Zugeordneter Wareneinsatz",
    "table.matchedGrossProfit": "Zugeordneter Bruttogewinn",
    "table.matchedRoi": "Zugeordneter ROI",
    "table.month": "Monat",
    "table.name": "Name",
    "table.netMargin": "Nettomarge",
    "table.netProfit": "Nettogewinn",
    "table.netRoi": "Netto-ROI",
    "table.other": "Sonstiges",
    "table.operationalCosts": "Operative Kosten",
    "table.onHand": "Auf Lager",
    "table.paymentRows": "Zahlungszeilen",
    "table.period": "Zeitraum",
    "table.product": "Produkt",
    "table.productCharges": "Produktumsatz",
    "table.promo": "Promo",
    "table.purchased": "Gekauft",
    "table.refunds": "Erstattungen",
    "table.reorderPoint": "Meldebestand",
    "table.reserved": "Reserviert",
    "table.quantity": "Menge",
    "table.revenueEur": "Umsatz EUR",
    "table.revenueGrossEur": "Bruttoumsatz EUR",
    "table.revenueNetEur": "Nettoumsatz EUR",
    "table.revenue": "Umsatz",
    "table.roi": "ROI",
    "table.rows": "Zeilen",
    "table.ordersUnits": "Bestellungen / Einheiten",
    "table.orderId": "Bestell-ID",
    "table.orderMatch": "Bestellabgleich",
    "table.orderUnits": "Bestelleinheiten",
    "table.paymentUnits": "Zahlungseinheiten",
    "table.refundGroups": "Erstattungsgruppen",
    "table.refundMatch": "Erstattungsabgleich",
    "table.returnFeeMatch": "Rücksendegebühren-Abgleich",
    "table.linkedSku": "Zugeordnete SKU",
    "table.sales": "Umsatz",
    "table.salesVat": "Umsatzsteuer",
    "table.salesCurrency": "Verkaufswährung",
    "table.sku": "SKU",
    "table.sold": "Verkauft",
    "table.source": "Quelle",
    "table.stockFlow": "Bestandsbewegung",
    "table.stockAlerts": "Bestandssignale",
    "table.status": "Status",
    "table.subtotal": "Zwischensumme",
    "table.total": "Summe",
    "table.totalEur": "Summe EUR",
    "table.vat": "MwSt.",
    "table.vatAmount": "MwSt.-Betrag",
    "table.vatRate": "MwSt.-Satz",
    "table.vatStatus": "MwSt.",
    "table.notes": "Notizen",
    "table.transfers": "Überträge",
    "table.type": "Typ",
    "table.units": "Einheiten",
    "table.unitsRefunded": "Erstattete Einheiten",
    "table.unitsSold": "Verkaufte Einheiten",
    "table.unknownTypes": "Unbekannte Typen",
  },
  uk: {
    "app.tagline": "Імпорт Amazon-обліку, закупівельні ціни та місячний cashflow.",
    "action.add": "Додати",
    "action.addOpeningLot": "Додати початкову партію",
    "action.addComponent": "Додати компонент",
    "action.saveBundle": "Зберегти бандл",
    "action.commit": "Зберегти",
    "action.commitRaw": "Зберегти raw",
    "action.mockCosts": "Mock цін",
    "action.preview": "Preview",
    "action.refresh": "Оновити",
    "action.refreshReports": "Оновити звіти",
    "action.search": "Пошук",
    "action.save": "Зберегти",
    "action.cancel": "Скасувати",
    "action.clear": "Очистити",
    "action.edit": "Редагувати",
    "action.delete": "Видалити",
    "action.manualStockEntry": "Ручний запис залишків",
    "action.downloadOrders": "Завантажити замовлення",
    "action.downloadReturns": "Завантажити повернення",
    "action.commitManualReport": "Зберегти ручний звіт",
    "action.syncOaCatalog": "Синхронізувати OA каталог",
    "action.syncInventory": "Синхронізувати залишки",
    "action.syncFbaInventory": "Синхронізувати FBA залишки",
    "action.syncEcbRates": "Синхронізувати курси ECB",
    "action.useMatch": "Застосувати",
    "action.viewLines": "Позиції",
    "allocation.byLineValue": "За вартістю рядка",
    "allocation.byQuantity": "За кількістю",
    "field.allocationMethod": "Метод розподілу",
    "field.costFile": "Файл цін CSV/XLSX",
    "field.csvReport": "CSV-звіт",
    "field.currency": "Валюта",
    "field.effectiveDate": "Дата дії",
    "field.endDate": "Дата завершення",
    "field.invoiceDate": "Дата інвойсу",
    "field.invoiceNumber": "Інвойс",
    "field.invoiceFile": "Інвойс CSV/XLSX/PDF",
    "field.invoiceNumber": "Номер інвойсу",
    "field.marketplace": "Маркетплейс",
    "field.ordersReport": "All Orders звіт",
    "field.rateToEur": "Курс до EUR",
    "field.reportType": "Тип звіту",
    "field.search": "Пошук",
    "field.startDate": "Дата початку",
    "field.supplier": "Постачальник",
    "field.supplierSku": "SKU постачальника",
    "field.productName": "Назва товару",
    "field.fulfillment": "Фулфілмент",
    "field.bundleSku": "Amazon SKU набору",
    "field.bundleName": "Назва набору",
    "field.componentSku": "SKU / EAN компонента",
    "field.componentQuantity": "Кількість компонента",
    "field.fbaPrepPerUnit": "FBA prep / одиницю EUR",
    "field.fbaStoragePerUnit": "FBA зберігання / продану одиницю EUR",
    "field.fbmPrepPerUnit": "FBM prep / одиницю EUR",
    "field.fbmPackagingPerUnit": "FBM пакування / одиницю EUR",
    "field.fbmOutboundPerUnit": "FBM відправлення / одиницю EUR",
    "field.fbmStoragePerUnit": "FBM зберігання / продану одиницю EUR",
    "field.amazonProductSearch": "Пошук Amazon товару",
    "field.invoiceProductSearch": "Пошук товару з інвойсу",
    "field.invoiceProductsSearch": "Пошук товару з інвойсу",
    "field.transactionCsv": "CSV транзакцій",
    "message.committedRaw": "Raw-звіт збережено.",
    "message.noData": "Немає даних",
    "message.noPreview": "Preview ще не завантажено.",
    "message.confirmDeletePayment": "Видалити цей Amazon Payments репорт? Його транзакції зникнуть з аналітики.",
    "message.confirmDeleteInvoice": "Видалити цей інвойс закупівлі? Позиції, створені ціни товарів і мапінги буде видалено.",
    "message.confirmDeleteCostImport": "Видалити цей імпорт закупівельних цін? Його ціни зникнуть з аналітики.",
    "message.confirmDeleteGenericReport": "Видалити цей raw-імпорт звіту?",
    "message.confirmDeleteInventory": "Видалити цей запис залишків?",
    "message.confirmDeleteOpeningLot": "Видалити цю початкову партію?",
    "message.confirmDeleteComponent": "Видалити цей компонент набору?",
    "recipe.chooseBundle": "Оберіть набір або створіть новий рецепт",
    "recipe.componentLines": "Компоненти",
    "recipe.totalUnits": "Одиниць у наборі",
    "recipe.estimatedCost": "Орієнтовна собівартість",
    "recipe.empty": "Компонентів ще немає. Додайте перший товар вище.",
    "recipe.purchased": "Закуплено у FIFO-партіях",
    "recipe.latestCost": "Ціна останньої партії",
    "recipe.unsaved": "Незбережені зміни",
    "message.selectInvoiceLine": "Спочатку обери товар з інвойсу.",
    "message.storageAllocationNote": "Поки немає щоденних snapshot залишків, зберігання оцінюється ставкою на продану одиницю.",
    "marketplace.eu": "Усі EU маркетплейси",
    "metric.withEan": "З EAN",
    "preview.detectedFields": "Розпізнані поля",
    "preview.expenses": "Витрати",
    "preview.invoice": "Інвойс",
    "preview.lines": "Рядки",
    "preview.noIssues": "Проблем не знайдено.",
    "preview.needsReview": "Потрібна перевірка",
    "preview.previewReady": "Preview готовий",
    "preview.quantity": "Кількість",
    "preview.subtotal": "Сума без ПДВ",
    "preview.products": "Товари",
    "preview.total": "Разом",
    "preview.unknownHeaders": "Невідомі колонки",
    "preview.validationErrors": "Помилки перевірки",
    "nav.dashboard": "Дашборд",
    "nav.imports": "Імпорти",
    "nav.operations": "Операції",
    "nav.overview": "Огляд",
    "nav.settings": "Налаштування",
    "period.all": "Весь час",
    "period.custom": "Свій період",
    "period.lastMonth": "Минулий місяць",
    "period.thisMonth": "Цей місяць",
    "paymentCategory.fbaFee": "FBA комісія",
    "paymentCategory.order": "Замовлення",
    "paymentCategory.other": "Інше",
    "paymentCategory.refund": "Повернення",
    "paymentCategory.returnFee": "Комісія повернення",
    "paymentCategory.serviceFee": "Сервісна комісія",
    "paymentCategory.transfer": "Переказ",
    "paymentCategory.unknown": "Невідомо",
    "report.customerReturns": "Повернення клієнтів",
    "report.reimbursements": "Компенсації",
    "report.serviceFees": "Сервісні збори",
    "section.amazonPayments": "Amazon платежі",
    "section.amazonConnector": "Amazon SP-API",
    "section.fxRates": "Курси валют",
    "section.generalCashflow": "Загальний cashflow",
    "section.inventory": "Товарні залишки",
    "section.openingInventoryLots": "Початкові партії залишків",
    "section.bundleRecipes": "Рецепти наборів",
    "section.invoiceLines": "Позиції інвойсу",
    "section.landedCost": "Landed Cost",
    "section.fulfillmentCosts": "Витрати фулфілменту",
    "section.paymentLines": "Рядки платежу",
    "section.productCosts": "Закупівельні ціни",
    "section.productMappings": "Мапінг товарів",
    "section.oaCatalog": "OA каталог",
    "section.amazonPnl": "Amazon P&L",
    "section.dataQuality": "Якість даних",
    "section.reconciliation": "Звірка Payments / Orders",
    "section.missingCosts": "Відсутні собівартості",
    "section.productProfitability": "Прибутковість товарів",
    "section.purchaseSummary": "Підсумок закупівель",
    "section.purchaseInvoices": "Інвойси закупівель",
    "section.reportPreview": "Preview звіту",
    "status.committed": "Збережено",
    "status.duplicate": "Вже імпортовано",
    "status.imported": "Імпортовано",
    "status.loaded": "Завантажено",
    "status.loading": "Завантаження",
    "status.mockCostsCreated": "Mock ціни створено",
    "status.mockingCosts": "Створюю mock ціни",
    "status.matched": "зіставлено",
    "status.missingCost": "немає ціни",
    "status.profitable": "прибутковий",
    "status.loss": "збитковий",
    "status.breakeven": "в нуль",
    "status.unknown": "невідомо",
    "status.unmapped": "не зіставлено",
    "status.unmatched": "не зіставлено",
    "status.quantityMismatch": "не збігається кількість",
    "status.ambiguous": "неоднозначно",
    "status.refundPending": "refund: окрема звірка",
    "status.returnFeePending": "return fee: окрема звірка",
    "status.healthy": "норма",
    "status.lowStock": "низький залишок",
    "status.outOfStock": "немає в наявності",
    "status.ready": "Готово",
    "status.saved": "Збережено",
    "status.saving": "Збереження",
    "status.uploading": "Завантаження",
    "vat.included": "з ПДВ",
    "vat.none": "без ПДВ",
    "vat.unknown": "ПДВ невідомо",
    "table.action": "Дія",
    "table.amazonProduct": "Amazon товар",
    "table.amazonFees": "Amazon комісії",
    "table.avgSellingPrice": "Сер. ціна продажу",
    "table.amazonOperatingResult": "Операційний результат Amazon",
    "table.baseCost": "Базова ціна",
    "table.cogsEur": "COGS EUR",
    "table.confidence": "Впевненість",
    "table.cost": "Ціна",
    "table.costCoverage": "Покриття цін",
    "table.costEur": "Ціна EUR",
    "table.date": "Дата",
    "table.effective": "Діє з",
    "table.estPayout": "Очік. виплата",
    "table.expenseCategory": "Категорія витрат",
    "table.fees": "Комісії",
    "table.file": "Файл",
    "table.fxToEur": "Курс до EUR",
    "table.generalTotalEur": "Загальна сума в EUR",
    "table.grossSales": "Валові продажі",
    "table.grossProfit": "Валовий прибуток",
    "table.id": "ID",
    "table.identifiers": "ASIN / SKU / EAN",
    "table.invoiceProduct": "Товар з інвойсу",
    "table.inboundShipping": "Транспорт",
    "table.inboundPerUnit": "Доставка / одиницю",
    "table.landedCost": "Landed cost",
    "table.available": "Доступно",
    "table.inbound": "В дорозі",
    "table.lineType": "Тип рядка",
    "table.lastSync": "Остання синхронізація",
    "table.market": "Маркет",
    "table.margin": "Маржа",
    "table.marketplaceCurrencyTotal": "{currency} сума у валюті маркету",
    "table.matchedCogs": "COGS зіставлених",
    "table.matchedGrossProfit": "Прибуток зіставлених",
    "table.matchedRoi": "ROI зіставлених",
    "table.month": "Місяць",
    "table.name": "Назва",
    "table.netMargin": "Чиста маржа",
    "table.netProfit": "Чистий прибуток",
    "table.netRoi": "Чистий ROI",
    "table.other": "Інше",
    "table.operationalCosts": "Операційні витрати",
    "table.onHand": "На складі",
    "table.paymentRows": "Рядки платежів",
    "table.period": "Період",
    "table.product": "Товар",
    "table.productCharges": "Продажі товару",
    "table.promo": "Промо",
    "table.purchased": "Куплено",
    "table.refunds": "Повернення",
    "table.reorderPoint": "Мін. залишок",
    "table.reserved": "Зарезервовано",
    "table.quantity": "Кількість",
    "table.revenueEur": "Дохід EUR",
    "table.revenueGrossEur": "Дохід з ПДВ EUR",
    "table.revenueNetEur": "Дохід без ПДВ EUR",
    "table.revenue": "Дохід",
    "table.roi": "ROI",
    "table.rows": "Рядки",
    "table.ordersUnits": "Замовлення / одиниці",
    "table.orderId": "Order ID",
    "table.orderMatch": "Зіставлення Orders",
    "table.orderUnits": "Одиниці Orders",
    "table.paymentUnits": "Одиниці Payments",
    "table.refundGroups": "Групи refund",
    "table.refundMatch": "Зіставлення refund",
    "table.returnFeeMatch": "Зіставлення return fee",
    "table.linkedSku": "Прив’язаний SKU",
    "table.sales": "Продажі",
    "table.salesVat": "ПДВ продажів",
    "table.salesCurrency": "Валюта продажу",
    "table.sku": "SKU",
    "table.sold": "Продано",
    "table.source": "Джерело",
    "table.stockFlow": "Рух залишків",
    "table.stockAlerts": "Сигнали залишків",
    "table.status": "Статус",
    "table.subtotal": "Сума без ПДВ",
    "table.total": "Разом",
    "table.totalEur": "Разом EUR",
    "table.vat": "ПДВ",
    "table.vatAmount": "Сума ПДВ",
    "table.vatRate": "Ставка ПДВ",
    "table.vatStatus": "ПДВ",
    "table.notes": "Нотатки",
    "table.transfers": "Перекази",
    "table.type": "Тип",
    "table.units": "Одиниці",
    "table.unitsRefunded": "Повернені одиниці",
    "table.unitsSold": "Продані одиниці",
    "table.unknownTypes": "Невідомі типи",
  },
};

const state = {
  language: localStorage.getItem("mirenelleOpsLanguage") || "en",
  activeSection: localStorage.getItem("mirenelleOpsSection") || "dashboard",
  periodPreset: localStorage.getItem("mirenelleOpsPeriodPreset") || "thisMonth",
  startDate: localStorage.getItem("mirenelleOpsStartDate") || "",
  endDate: localStorage.getItem("mirenelleOpsEndDate") || "",
  purchaseSummary: null,
  amazonPnlSummary: null,
  dataQualitySummary: null,
  profitSummary: null,
  inventoryRows: [],
  bundleComponents: [],
  bundleCandidates: { bundles: [], components: [] },
  activeBundleSku: null,
  bundleDraft: [],
  bundleDraftOriginalSku: null,
  bundleDraftDirty: false,
  paymentRows: [],
  selectedPaymentId: null,
  invoiceRows: [],
  selectedInvoiceId: null,
  selectedMappingInvoiceLineId: null,
  editingInvoiceProductLineId: null,
  unmappedInvoiceLines: [],
  productCostRows: [],
};

const sectionTitleKey = {
  dashboard: "nav.dashboard",
  cashflow: "section.generalCashflow",
  profitability: "section.productProfitability",
  payments: "section.amazonPayments",
  invoices: "section.purchaseInvoices",
  costs: "section.productCosts",
  mappings: "section.productMappings",
  inventory: "section.inventory",
  connector: "section.amazonConnector",
  settings: "nav.settings",
};

const t = (key, params = {}) => {
  const template = translations[state.language]?.[key] || translations.en[key] || key;
  return Object.entries(params).reduce(
    (value, [name, replacement]) => value.replaceAll(`{${name}}`, replacement),
    template,
  );
};

const localeByLanguage = {
  en: "en-US",
  de: "de-DE",
  uk: "uk-UA",
};

function applyTranslations() {
  document.documentElement.lang = state.language;
  document.querySelectorAll("[data-i18n]").forEach((element) => {
    element.textContent = t(element.dataset.i18n);
  });
  document.querySelectorAll("[data-i18n-placeholder]").forEach((element) => {
    element.placeholder = t(element.dataset.i18nPlaceholder);
  });
  document.querySelectorAll("[data-status-key]").forEach((element) => {
    element.textContent = t(element.dataset.statusKey);
  });
  updatePageTitle();
}

function isoDate(date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

function getMonthRange(offset = 0) {
  const now = new Date();
  const start = new Date(now.getFullYear(), now.getMonth() + offset, 1);
  const end = new Date(now.getFullYear(), now.getMonth() + offset + 1, 0);
  return { start: isoDate(start), end: isoDate(end) };
}

function syncPeriodControls() {
  const preset = document.getElementById("periodPreset");
  const start = document.getElementById("startDateFilter");
  const end = document.getElementById("endDateFilter");
  if (!preset || !start || !end) return;

  if (state.periodPreset === "thisMonth") {
    const range = getMonthRange(0);
    state.startDate = range.start;
    state.endDate = range.end;
  } else if (state.periodPreset === "lastMonth") {
    const range = getMonthRange(-1);
    state.startDate = range.start;
    state.endDate = range.end;
  } else if (state.periodPreset === "all") {
    state.startDate = "";
    state.endDate = "";
  }

  preset.value = state.periodPreset;
  start.value = state.startDate;
  end.value = state.endDate;
  const connectorStart = document.querySelector('#amazonOrdersSyncForm input[name="start_date"]');
  const connectorEnd = document.querySelector('#amazonOrdersSyncForm input[name="end_date"]');
  if (connectorStart && !connectorStart.value) connectorStart.value = state.startDate;
  if (connectorEnd && !connectorEnd.value) connectorEnd.value = state.endDate;
  const isCustom = state.periodPreset === "custom";
  start.disabled = !isCustom;
  end.disabled = !isCustom;
}

function persistPeriod() {
  localStorage.setItem("mirenelleOpsPeriodPreset", state.periodPreset);
  localStorage.setItem("mirenelleOpsStartDate", state.startDate);
  localStorage.setItem("mirenelleOpsEndDate", state.endDate);
}

function reportQueryParams(extra = {}) {
  const params = new URLSearchParams();
  if (state.startDate) params.set("start_date", state.startDate);
  if (state.endDate) params.set("end_date", state.endDate);
  Object.entries(extra).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== "") params.set(key, value);
  });
  const query = params.toString();
  return query ? `?${query}` : "";
}

const money = (value, currency) =>
  new Intl.NumberFormat(localeByLanguage[state.language] || "en-US", {
    style: "currency",
    currency,
    maximumFractionDigits: 2,
  }).format(Number(value || 0));

const text = (value) => {
  if (value === null || value === undefined || value === "") return "-";
  return String(value);
};

const purchaseSummaryPeriod = (value) => (value === "all" ? t("period.all") : text(value));

function lineTypeLabel(value) {
  const labels = {
    product: {
      en: "Product",
      de: "Produkt",
      uk: "Товар",
    },
    inbound_shipping: {
      en: "Inbound shipping",
      de: "Transport",
      uk: "Транспорт",
    },
    fulfillment_fee: {
      en: "Fulfillment",
      de: "Fulfillment",
      uk: "Фулфілмент",
    },
    marketplace_fee: {
      en: "Marketplace fee",
      de: "Marketplace-Gebühr",
      uk: "Маркетплейс комісія",
    },
    service: {
      en: "Service",
      de: "Dienstleistung",
      uk: "Послуга",
    },
    other: {
      en: "Other",
      de: "Sonstiges",
      uk: "Інше",
    },
  };
  return labels[value]?.[state.language] || labels[value]?.en || text(value);
}

const escapeHtml = (value) =>
  text(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");

function renderIdentifiers(row) {
  return `
    <div class="identifierStack">
      <span><b>ASIN</b>${escapeHtml(row.asin)}</span>
      <span><b>SKU</b>${escapeHtml(row.sku)}</span>
      <span><b>EAN</b>${escapeHtml(row.ean)}</span>
    </div>
  `;
}

const setStatus = (id, message, isError = false, isKey = false) => {
  const element = document.getElementById(id);
  element.textContent = isKey ? t(message) : message;
  if (isKey) {
    element.dataset.statusKey = message;
  } else {
    delete element.dataset.statusKey;
  }
  element.classList.toggle("error", isError);
};

async function requestJson(url, options = {}) {
  const response = await fetch(url, options);
  const data = await response.json();
  if (!response.ok) {
    const detail = typeof data.detail === "string" ? data.detail : JSON.stringify(data.detail);
    throw new Error(detail || response.statusText);
  }
  return data;
}

function renderRows(targetId, rows, render) {
  const target = document.getElementById(targetId);
  target.innerHTML = rows.length
    ? rows.map(render).join("")
    : `<tr><td class="muted" colspan="12">${t("message.noData")}</td></tr>`;
  applySearchFilter();
}

function bundleRecipeGroups() {
  const groups = new Map();
  state.bundleComponents.forEach((component) => {
    if (!groups.has(component.bundle_sku)) {
      groups.set(component.bundle_sku, {
        sku: component.bundle_sku,
        name: component.bundle_name,
        components: [],
      });
    }
    const group = groups.get(component.bundle_sku);
    if (!group.name && component.bundle_name) group.name = component.bundle_name;
    group.components.push(component);
  });
  return [...groups.values()];
}

function componentCandidate(sku) {
  return state.bundleCandidates.components.find((row) => row.sku === sku);
}

function recipeEstimatedCosts(components) {
  const totals = new Map();
  components.forEach((component) => {
    const candidate = componentCandidate(component.component_sku);
    if (!candidate) return;
    const currency = candidate.currency || "EUR";
    const value = Number(component.component_quantity || 0) * Number(candidate.latest_unit_cost || 0);
    totals.set(currency, (totals.get(currency) || 0) + value);
  });
  return [...totals.entries()].map(([currency, value]) => money(value, currency)).join(" + ") || "-";
}

function loadBundleDraft(group = null) {
  state.bundleDraft = group
    ? group.components.map((component) => ({
      component_sku: component.component_sku,
      component_quantity: Number(component.component_quantity),
    }))
    : [];
  state.bundleDraftOriginalSku = group?.sku || null;
  state.bundleDraftDirty = false;
}

function renderBundleRecipes() {
  const groups = bundleRecipeGroups();
  const recipeCount = document.getElementById("recipeCount");
  const cards = document.getElementById("bundleRecipeCards");
  const summary = document.getElementById("activeRecipeSummary");
  const componentCards = document.getElementById("activeRecipeComponents");
  const form = document.getElementById("bundleComponentForm");
  if (!recipeCount || !cards || !summary || !componentCards || !form) return;

  if (state.activeBundleSku && !groups.some((group) => group.sku === state.activeBundleSku)) {
    state.activeBundleSku = null;
  }
  if (!state.activeBundleSku && groups.length) state.activeBundleSku = groups[0].sku;

  recipeCount.textContent = String(groups.length);
  cards.innerHTML = groups.length
    ? groups.map((group) => {
      const totalUnits = group.components.reduce(
        (sum, component) => sum + Number(component.component_quantity || 0),
        0,
      );
      return `
        <button type="button" class="recipeCard ${group.sku === state.activeBundleSku ? "active" : ""}" data-select-bundle="${escapeHtml(group.sku)}">
          <span class="recipeCardTop"><strong>${escapeHtml(group.name || group.sku)}</strong><small>${group.components.length}</small></span>
          <span class="recipeCardSku">${escapeHtml(group.sku)}</span>
          <span class="recipeCardMeta">${integer(totalUnits)} · ${t("recipe.totalUnits")}</span>
        </button>
      `;
    }).join("")
    : `
      <button type="button" class="recipeEmptyAction" data-start-bundle-recipe>
        <span>＋</span>
        <strong>${t("recipe.chooseBundle")}</strong>
      </button>
    `;

  const active = groups.find((group) => group.sku === state.activeBundleSku);
  if (active && state.bundleDraftOriginalSku !== active.sku) {
    loadBundleDraft(active);
    form.elements.namedItem("bundle_sku").value = active.sku;
    form.elements.namedItem("bundle_name").value = active.name || "";
  }

  const draft = state.bundleDraft;
  const saveButton = document.getElementById("saveBundleRecipeButton");
  const draftStatus = document.getElementById("bundleDraftStatus");
  if (saveButton) saveButton.disabled = draft.length === 0;
  if (draftStatus) draftStatus.textContent = state.bundleDraftDirty ? t("recipe.unsaved") : "";

  if (!draft.length) {
    summary.innerHTML = "";
    summary.classList.add("hidden");
    componentCards.innerHTML = `<div class="recipeEmptyState">${t("recipe.empty")}</div>`;
    return;
  }

  summary.classList.remove("hidden");
  const bundleSku = form.elements.namedItem("bundle_sku").value.trim();
  const bundleName = form.elements.namedItem("bundle_name").value.trim();
  const totalUnits = draft.reduce(
    (sum, component) => sum + Number(component.component_quantity || 0),
    0,
  );
  summary.innerHTML = `
    <div class="recipeTitle">
      <span>${escapeHtml(bundleSku)}</span>
      <strong>${escapeHtml(bundleName || bundleSku)}</strong>
    </div>
    <div class="recipeMetric"><span>${t("recipe.componentLines")}</span><strong>${draft.length}</strong></div>
    <div class="recipeMetric"><span>${t("recipe.totalUnits")}</span><strong>${integer(totalUnits)}</strong></div>
    <div class="recipeMetric"><span>${t("recipe.estimatedCost")}</span><strong>${recipeEstimatedCosts(draft)}</strong></div>
  `;
  componentCards.innerHTML = draft.length
    ? draft.map((component, index) => {
      const candidate = componentCandidate(component.component_sku);
      return `
        <article class="componentCard">
          <div class="componentIdentity">
            <span class="componentSku">${escapeHtml(component.component_sku)}</span>
            <strong>${escapeHtml(candidate?.product_name || component.component_sku)}</strong>
            <div class="componentMeta">
              <span>${t("recipe.purchased")}: ${candidate ? integer(candidate.available_quantity) : "-"}</span>
              <span>${t("recipe.latestCost")}: ${candidate ? money(candidate.latest_unit_cost, candidate.currency) : "-"}</span>
            </div>
          </div>
          <div class="componentQuantity"><span>×</span><strong>${integer(component.component_quantity)}</strong></div>
          <button type="button" class="compactButton dangerButton" data-remove-draft-component="${index}">${t("action.delete")}</button>
        </article>
      `;
    }).join("")
    : `<div class="recipeEmptyState">${t("recipe.empty")}</div>`;
}

function renderBundleCandidateOptions() {
  const componentOptions = document.getElementById("componentSkuOptions");
  if (!componentOptions) return;
  componentOptions.innerHTML = state.bundleCandidates.components.map((row) => (
    `<option value="${escapeHtml(row.sku)}">${escapeHtml(row.product_name)} · ${integer(row.available_quantity)} · ${money(row.latest_unit_cost, row.currency)}</option>`
  )).join("");
}

function renderBundleSkuSuggestions(query = "") {
  const target = document.getElementById("bundleSkuSuggestions");
  if (!target) return;
  const normalized = query.trim().toLocaleLowerCase();
  if (normalized.length < 2) {
    target.innerHTML = "";
    target.classList.remove("open");
    return;
  }
  const matches = state.bundleCandidates.bundles.filter((row) => (
    row.sku.toLocaleLowerCase().includes(normalized)
      || (row.product_name || "").toLocaleLowerCase().includes(normalized)
  )).slice(0, 8);
  target.innerHTML = matches.length
    ? matches.map((row) => `
      <button type="button" data-bundle-suggestion="${escapeHtml(row.sku)}">
        <strong>${escapeHtml(row.sku)}</strong>
        <span>${escapeHtml(row.product_name || row.sku)}</span>
      </button>
    `).join("")
    : `<div class="recipeSuggestionEmpty">${t("message.noData")}</div>`;
  target.classList.add("open");
}

function startBundleRecipe() {
  state.activeBundleSku = null;
  loadBundleDraft();
  const form = document.getElementById("bundleComponentForm");
  const bundleSku = form?.elements.namedItem("bundle_sku");
  const bundleName = form?.elements.namedItem("bundle_name");
  if (!bundleSku) return;
  bundleSku.value = "";
  if (bundleName) bundleName.value = "";
  renderBundleSkuSuggestions("");
  renderBundleRecipes();
  bundleSku.focus();
}

function updatePageTitle() {
  const title = document.getElementById("pageTitle");
  if (title) title.textContent = t(sectionTitleKey[state.activeSection] || "nav.dashboard");
}

function showSection(sectionName, resetScroll = false) {
  if (!document.getElementById(`section-${sectionName}`)) {
    sectionName = "dashboard";
  }
  state.activeSection = sectionName;
  localStorage.setItem("mirenelleOpsSection", sectionName);
  document.querySelectorAll(".pageSection").forEach((section) => {
    section.classList.toggle("active", section.id === `section-${sectionName}`);
  });
  document.querySelectorAll(".navItem").forEach((button) => {
    button.classList.toggle("active", button.dataset.sectionTarget === sectionName);
  });
  updatePageTitle();
  applySearchFilter();
  if (resetScroll) {
    window.scrollTo({ top: 0, left: 0, behavior: "auto" });
  }
}

function applySearchFilter() {
  const search = document.getElementById("globalSearch");
  const query = (search?.value || "").trim().toLowerCase();
  document.querySelectorAll(".pageSection.active tbody tr").forEach((row) => {
    if (!query || row.textContent.toLowerCase().includes(query)) {
      row.hidden = false;
    } else {
      row.hidden = true;
    }
  });
}

async function loadPayments() {
  const data = await requestJson(`/imports/amazon-payments${reportQueryParams()}`);
  state.paymentRows = data.rows;
  renderRows("paymentImports", data.rows, (row) => `
    <tr data-payment-row="${row.import_id}" class="${String(row.import_id) === String(state.selectedPaymentId) ? "selectedRow" : ""}">
      <td>${row.import_id}</td>
      <td>${row.marketplace}</td>
      <td class="num">${row.row_count}</td>
      <td>${text(row.report_period_start)} - ${text(row.report_period_end)}</td>
      <td>${row.filename}</td>
      <td class="actionsCell">
        <button type="button" class="compactButton" data-payment-lines="${row.import_id}">${t("action.viewLines")}</button>
        <button
          type="button"
          class="compactButton dangerButton"
          data-delete-payment="${row.import_id}"
          data-delete-payment-name="${escapeHtml(row.filename)}"
        >${t("action.delete")}</button>
      </td>
    </tr>
  `);
}

async function loadPaymentLines(importId) {
  setStatus("paymentLinesStatus", "status.loading", false, true);
  state.selectedPaymentId = String(importId);
  document.querySelectorAll("#paymentImports tr").forEach((row) => {
    row.classList.toggle("selectedRow", row.dataset.paymentRow === String(importId));
  });
  const selected = state.paymentRows.find((row) => String(row.import_id) === String(importId));
  const panel = document.getElementById("paymentLinesPanel");
  panel.classList.remove("hidden");
  document.getElementById("selectedPaymentInfo").innerHTML = selected
    ? `
      <div><span>ID</span><strong>${selected.import_id}</strong></div>
      <div><span>${t("field.marketplace")}</span><strong>${escapeHtml(selected.marketplace)}</strong></div>
      <div><span>${t("table.period")}</span><strong>${text(selected.report_period_start)} - ${text(selected.report_period_end)}</strong></div>
      <div><span>${t("table.file")}</span><strong>${escapeHtml(selected.filename)}</strong></div>
      <div><span>${t("table.rows")}</span><strong>${selected.row_count}</strong></div>
    `
    : "";
  const data = await requestJson(`/imports/amazon-payments/${importId}/lines`);
  renderRows("paymentLineRows", data.rows, (row) => `
    <tr>
      <td>${text(row.transaction_date)}</td>
      <td>${text(row.transaction_status)}</td>
      <td>${text(row.transaction_type)}</td>
      <td>${text(row.sku)}</td>
      <td class="num">${text(row.quantity)}</td>
      <td>${text(row.fulfillment_channel)}</td>
      <td>${text(row.product_details)}</td>
      <td class="num">${money(row.product_charges, row.currency)}</td>
      <td class="num">${money(row.promotional_rebates, row.currency)}</td>
      <td class="num">${money(row.amazon_fees, row.currency)}</td>
      <td class="num">${money(row.other_amount, row.currency)}</td>
      <td class="num">${money(row.total_amount, row.currency)}</td>
    </tr>
  `);
  setStatus("paymentLinesStatus", "status.loaded", false, true);
  panel.scrollIntoView({ block: "nearest", behavior: "smooth" });
}

function hidePaymentLines() {
  state.selectedPaymentId = null;
  document.querySelectorAll("#paymentImports tr").forEach((row) => {
    row.classList.remove("selectedRow");
  });
  document.getElementById("paymentLinesPanel").classList.add("hidden");
  document.getElementById("selectedPaymentInfo").innerHTML = "";
  renderRows("paymentLineRows", [], () => "");
  setStatus("paymentLinesStatus", "status.ready", false, true);
}

async function loadCosts() {
  const lots = await requestJson("/imports/product-costs/lots?limit=5000");
  state.productCostRows = lots.rows;
  renderRows("costLots", lots.rows, (row) => `
    <tr>
      <td>${row.purchase_date}</td>
      <td>${text(row.sku)}</td>
      <td>${text(row.ean)}</td>
      <td>${text(row.product_name)}</td>
      <td class="num">${row.quantity_received}</td>
      <td class="num">${row.base_unit_cost === null ? "-" : money(row.base_unit_cost, row.currency)}</td>
      <td class="num">${money(row.inbound_shipping_per_unit, row.currency)}</td>
      <td class="num">${money(row.landed_unit_cost, row.currency)}</td>
      <td>${row.currency}</td>
      <td>${text(row.source)}</td>
      <td>${text(row.supplier_name)}</td>
      <td>${text(row.invoice_number)}</td>
      <td>
        ${row.product_cost_id ? `<button type="button" class="compactButton" data-edit-cost="${row.product_cost_id}">${t("action.edit")}</button>` : "-"}
      </td>
    </tr>
  `);
}

async function loadInvoices() {
  const data = await requestJson(`/imports/purchase-invoices${reportQueryParams()}`);
  state.invoiceRows = data.rows;
  renderRows("invoiceImports", data.rows, (row) => `
    <tr data-invoice-row="${row.invoice_id}" class="${String(row.invoice_id) === String(state.selectedInvoiceId) ? "selectedRow" : ""}">
      <td>${row.invoice_id}</td>
      <td>${text(row.supplier_name)}</td>
      <td>${text(row.invoice_number)}</td>
      <td>${text(row.invoice_date)}</td>
      <td class="num">${row.row_count}</td>
      <td>${vatStatusLabel(row.vat_status)}</td>
      <td class="num">${row.vat_amount === null ? "-" : money(row.vat_amount, row.currency)}</td>
      <td class="num">${row.total_amount === null ? "-" : money(row.total_amount, row.currency)}</td>
      <td class="actionsCell">
        <button type="button" class="compactButton" data-invoice-lines="${row.invoice_id}">${t("action.viewLines")}</button>
        <button
          type="button"
          class="compactButton dangerButton"
          data-delete-invoice="${row.invoice_id}"
          data-delete-invoice-name="${escapeHtml(row.invoice_number || row.filename)}"
        >${t("action.delete")}</button>
      </td>
    </tr>
  `);

  const summary = await requestJson(`/reports/purchase-summary${reportQueryParams()}`);
  state.purchaseSummary = summary;
  updateDashboardPurchase();
  renderRows("purchaseSummaryRows", summary.rows, (row) => `
    <tr>
      <td>${purchaseSummaryPeriod(row.month)}</td>
      <td>${text(row.supplier_name)}</td>
      <td class="num">${row.quantity}</td>
      <td class="num">${money(row.product_subtotal_amount ?? row.subtotal_amount, row.currency)}</td>
      <td class="num">${money(row.expense_subtotal_amount ?? 0, row.currency)}</td>
      <td class="num">${money(row.inbound_shipping_amount ?? 0, row.currency)}</td>
      <td class="num">${money(row.total_amount, row.currency)}</td>
    </tr>
  `);
}

async function loadInvoiceLines(invoiceId) {
  setStatus("invoiceLinesStatus", "status.loading", false, true);
  state.selectedInvoiceId = String(invoiceId);
  document.querySelectorAll("#invoiceImports tr").forEach((row) => {
    row.classList.toggle("selectedRow", row.dataset.invoiceRow === String(invoiceId));
  });
  const selected = state.invoiceRows.find((row) => String(row.invoice_id) === String(invoiceId));
  const panel = document.getElementById("invoiceLinesPanel");
  panel.classList.remove("hidden");
  document.getElementById("selectedInvoiceInfo").innerHTML = selected
    ? `
      <div><span>ID</span><strong>${selected.invoice_id}</strong></div>
      <div><span>${t("field.supplier")}</span><strong>${escapeHtml(selected.supplier_name)}</strong></div>
      <div><span>${t("field.invoiceNumber")}</span><strong>${escapeHtml(selected.invoice_number)}</strong></div>
      <div><span>${t("field.invoiceDate")}</span><strong>${escapeHtml(selected.invoice_date)}</strong></div>
      <div><span>${t("table.vatStatus")}</span><strong>${vatStatusLabel(selected.vat_status)}</strong></div>
      <div><span>${t("table.subtotal")}</span><strong>${selected.subtotal_amount === null ? "-" : money(selected.subtotal_amount, selected.currency)}</strong></div>
      <div><span>${t("table.vatAmount")}</span><strong>${selected.vat_amount === null ? "-" : money(selected.vat_amount, selected.currency)}</strong></div>
      <div><span>${t("table.total")}</span><strong>${selected.total_amount === null ? "-" : money(selected.total_amount, selected.currency)}</strong></div>
    `
    : "";
  const data = await requestJson(`/imports/purchase-invoices/${invoiceId}/lines`);
  renderRows("invoiceLineRows", data.rows, (row) => `
    <tr>
      <td>${lineTypeLabel(row.line_type)}</td>
      <td>${text(row.sku || row.supplier_sku)}</td>
      <td>${text(row.ean)}</td>
      <td>${text(row.product_name)}</td>
      <td class="num">${row.quantity}</td>
      <td class="num">${money(row.unit_cost, row.currency)}</td>
      <td class="num">${row.line_net_amount === null ? "-" : money(row.line_net_amount, row.currency)}</td>
      <td class="num">${row.vat_rate_percent === null ? "-" : `${row.vat_rate_percent}%`}</td>
      <td class="num">${row.vat_amount === null ? "-" : money(row.vat_amount, row.currency)}</td>
      <td class="num">${row.line_gross_amount === null ? "-" : money(row.line_gross_amount, row.currency)}</td>
      <td>${text(row.expense_category)}</td>
    </tr>
  `);
  setStatus("invoiceLinesStatus", "status.loaded", false, true);
  panel.scrollIntoView({ block: "nearest", behavior: "smooth" });
}

function hideInvoiceLines() {
  state.selectedInvoiceId = null;
  document.querySelectorAll("#invoiceImports tr").forEach((row) => {
    row.classList.remove("selectedRow");
  });
  document.getElementById("invoiceLinesPanel").classList.add("hidden");
  document.getElementById("selectedInvoiceInfo").innerHTML = "";
  renderRows("invoiceLineRows", [], () => "");
  setStatus("invoiceLinesStatus", "status.ready", false, true);
}

function updateDashboardPurchase() {
  const summary = state.purchaseSummary;
  if (!summary) return;
  const subtotal = document.getElementById("dashboardPurchaseSubtotal");
  const quantity = document.getElementById("dashboardPurchaseQty");
  const rows = document.getElementById("dashboardPurchaseRows");
  const subtotalEur = summary.rows.reduce((sum, row) => sum + (row.currency === "EUR" ? row.subtotal_amount : 0), 0);
  const productSubtotalEur = summary.rows.reduce((sum, row) => sum + (row.currency === "EUR" ? (row.product_subtotal_amount ?? row.subtotal_amount) : 0), 0);
  const qty = summary.rows.reduce((sum, row) => sum + row.quantity, 0);
  const lineCount = summary.rows.reduce((sum, row) => sum + row.lines, 0);
  if (subtotal) subtotal.textContent = money(productSubtotalEur || subtotalEur, "EUR");
  if (quantity) quantity.textContent = qty;
  if (rows) rows.textContent = lineCount;
}

async function loadProductMappings() {
  const invoiceQuery = document.getElementById("invoiceLineSearch")?.value.trim() || "";
  const amazonQuery = document.getElementById("amazonProductSearch")?.value.trim() || "";
  const invoiceProducts = await requestJson(`/product-mappings/invoice-products${invoiceQuery ? `?query=${encodeURIComponent(invoiceQuery)}` : ""}`);
  state.unmappedInvoiceLines = invoiceProducts.rows;
  if (!invoiceProducts.rows.some((row) => String(row.invoice_line_id) === String(state.selectedMappingInvoiceLineId))) {
    state.selectedMappingInvoiceLineId = invoiceProducts.rows[0]?.invoice_line_id || null;
  }
  renderManualInvoiceLines(invoiceProducts.rows);

  try {
    const [suggestions, mappings, amazonProducts] = await Promise.all([
      requestJson("/product-mappings/suggestions"),
      requestJson("/product-mappings"),
      requestJson(`/product-mappings/amazon-products${amazonQuery ? `?query=${encodeURIComponent(amazonQuery)}` : ""}`),
    ]);
    renderManualAmazonProducts(amazonProducts.rows);
    renderRows("mappingSuggestions", suggestions.rows, (row) => `
      <tr>
        <td>${text(row.invoice_product_name)}</td>
        <td>${text(row.amazon_product_details)}</td>
        <td class="num">${row.confidence}%</td>
        <td>
          <button type="button" class="compactButton" data-map-line="${row.invoice_line_id}" data-amazon-product="${encodeURIComponent(row.amazon_product_details)}" data-confidence="${row.confidence}">
            ${t("action.useMatch")}
          </button>
        </td>
      </tr>
    `);
    renderRows("productMappings", mappings.rows, (row) => `
      <tr>
        <td>${text(row.supplier_name)}</td>
        <td>${text(row.invoice_product_name)}</td>
        <td>${text(row.amazon_product_details)}</td>
        <td>${text(row.match_method)}</td>
      </tr>
    `);
  } catch (error) {
    renderManualAmazonProducts([]);
    renderRows("mappingSuggestions", [], () => "");
    renderRows("productMappings", [], () => "");
    setStatus("mappingStatus", error.message, true);
  }
}

function renderManualInvoiceLines(rows) {
  renderRows("manualInvoiceLines", rows, (row) => `
    <tr data-manual-invoice-line="${row.invoice_line_id}" class="${String(row.invoice_line_id) === String(state.selectedMappingInvoiceLineId) ? "selectedRow" : ""}">
      <td>${text(row.supplier_name)}</td>
      <td>${text(row.invoice_number)}</td>
      <td>${text(row.supplier_sku || row.sku)}</td>
      <td>${text(row.ean)}</td>
      <td>${text(row.invoice_product_name)}</td>
      <td class="num">${row.quantity}</td>
      <td class="num">${money(row.unit_cost, row.currency)}</td>
      <td>${row.is_mapped ? t("status.matched") : t("status.unmapped")}${row.amazon_product_details ? `<br><span class="muted">${escapeHtml(row.amazon_product_details)}</span>` : ""}</td>
      <td>
        <button type="button" class="compactButton" data-edit-invoice-product="${row.invoice_line_id}">${t("action.edit")}</button>
      </td>
    </tr>
  `);
}

function clearInvoiceProductEditForm() {
  state.editingInvoiceProductLineId = null;
  document.getElementById("invoiceProductEditId").value = "";
  document.getElementById("invoiceProductEditSupplierSku").value = "";
  document.getElementById("invoiceProductEditSku").value = "";
  document.getElementById("invoiceProductEditEan").value = "";
  document.getElementById("invoiceProductEditName").value = "";
  document.getElementById("invoiceProductEditForm").classList.add("hidden");
}

function openInvoiceProductEditForm(row) {
  state.editingInvoiceProductLineId = row.invoice_line_id;
  document.getElementById("invoiceProductEditId").value = row.invoice_line_id;
  document.getElementById("invoiceProductEditSupplierSku").value = row.supplier_sku || "";
  document.getElementById("invoiceProductEditSku").value = row.sku || "";
  document.getElementById("invoiceProductEditEan").value = row.ean || "";
  document.getElementById("invoiceProductEditName").value = row.invoice_product_name || "";
  document.getElementById("invoiceProductEditForm").classList.remove("hidden");
  document.getElementById("invoiceProductEditName").focus();
}

function renderManualAmazonProducts(rows) {
  renderRows("manualAmazonProducts", rows, (row) => `
    <tr>
      <td>${text(row.amazon_product_details)}</td>
      <td class="num">${row.transaction_rows}</td>
      <td class="num">${money(row.revenue_eur_hint, "EUR")}</td>
      <td>
        <button type="button" class="compactButton" data-manual-map-product="${encodeURIComponent(row.amazon_product_details)}">
          ${t("action.useMatch")}
        </button>
      </td>
    </tr>
  `);
}

function inventoryStatusLabel(status) {
  if (status === "healthy") return t("status.healthy");
  if (status === "low_stock") return t("status.lowStock");
  if (status === "out_of_stock") return t("status.outOfStock");
  return text(status);
}

const integer = (value) => new Intl.NumberFormat(localeByLanguage[state.language] || "en-US").format(Number(value || 0));

function renderInventoryTotals(summary, rows = []) {
  const totalPurchased = rows.reduce((sum, row) => sum + Number(row.purchased_quantity || 0), 0);
  const totalSold = rows.reduce((sum, row) => sum + Number(row.sold_quantity || 0), 0);
  const totalReserved = rows.reduce((sum, row) => sum + Number(row.quantity_reserved || 0), 0);
  const totalReorder = rows.reduce((sum, row) => sum + Number(row.reorder_point || 0), 0);
  document.getElementById("inventoryTotals").innerHTML = `
    <article class="metricTile">
      <div class="metricHead">
        <strong>${t("section.inventory")}</strong>
        <span>${t("table.onHand")}</span>
      </div>
      <div class="metricBody">
        <div class="wideMetric"><span>${t("table.onHand")}</span><strong>${integer(summary.total_on_hand)}</strong></div>
        <div><span>${t("table.available")}</span><strong>${integer(summary.total_available)}</strong></div>
        <div><span>${t("table.product")}</span><strong>${integer(summary.products)}</strong></div>
      </div>
    </article>
    <article class="metricTile">
      <div class="metricHead">
        <strong>${t("table.stockFlow")}</strong>
        <span>${t("table.purchased")} / ${t("table.sold")}</span>
      </div>
      <div class="metricBody">
        <div class="wideMetric"><span>${t("table.purchased")}</span><strong>${integer(totalPurchased)}</strong></div>
        <div><span>${t("table.sold")}</span><strong>${integer(totalSold)}</strong></div>
        <div><span>${t("table.reserved")}</span><strong>${integer(totalReserved)}</strong></div>
      </div>
    </article>
    <article class="metricTile">
      <div class="metricHead">
        <strong>${t("table.inbound")}</strong>
        <span>${t("table.reorderPoint")}</span>
      </div>
      <div class="metricBody">
        <div class="wideMetric"><span>${t("table.inbound")}</span><strong>${integer(summary.total_inbound)}</strong></div>
        <div><span>${t("table.reorderPoint")}</span><strong>${integer(totalReorder)}</strong></div>
        <div><span>${t("table.available")}</span><strong>${integer(summary.total_available)}</strong></div>
      </div>
    </article>
    <article class="metricTile">
      <div class="metricHead">
        <strong>${t("table.stockAlerts")}</strong>
        <span>${t("table.status")}</span>
      </div>
      <div class="metricBody">
        <div class="wideMetric"><span>${t("status.lowStock")}</span><strong>${integer(summary.low_stock)}</strong></div>
        <div><span>${t("status.outOfStock")}</span><strong>${integer(summary.out_of_stock)}</strong></div>
        <div><span>${t("status.healthy")}</span><strong>${integer(Math.max(Number(summary.products || 0) - Number(summary.low_stock || 0) - Number(summary.out_of_stock || 0), 0))}</strong></div>
      </div>
    </article>
  `;
}

async function loadInventory() {
  const [summary, items, openingLots, bundleComponents, bundleCandidates] = await Promise.all([
    requestJson("/inventory/summary"),
    requestJson("/inventory/items"),
    requestJson("/inventory/opening-lots"),
    requestJson("/inventory/bundle-components"),
    requestJson("/inventory/bundle-candidates"),
  ]);
  state.inventoryRows = items.rows;
  state.bundleComponents = bundleComponents.rows;
  state.bundleCandidates = bundleCandidates;
  const openingDate = document.querySelector('#openingLotForm input[name="purchase_date"]');
  if (openingDate && !openingDate.value) {
    openingDate.value = state.startDate || isoDate(new Date());
  }
  renderInventoryTotals(summary, items.rows);
  renderRows("inventoryRows", items.rows, (row) => `
    <tr>
      <td class="productNameCell" title="${escapeHtml(text(row.product_name))}"><span>${text(row.product_name)}</span></td>
      <td>${renderIdentifiers(row)}</td>
      <td>${text(row.marketplace)}</td>
      <td>${text(row.fulfillment_channel)}</td>
      <td class="num">${integer(row.purchased_quantity)}</td>
      <td class="num">${integer(row.sold_quantity)}</td>
      <td class="num">${integer(row.quantity_on_hand)}</td>
      <td class="num">${integer(row.quantity_available)}</td>
      <td class="num">${integer(row.quantity_reserved)}</td>
      <td class="num">${integer(row.quantity_inbound)}</td>
      <td class="num">${integer(row.reorder_point)}</td>
      <td><span class="statusPill ${row.status}">${inventoryStatusLabel(row.status)}</span></td>
      <td>${new Date(row.updated_at).toLocaleString(localeByLanguage[state.language] || "en-US")}</td>
      <td>
        <button type="button" class="compactButton" data-edit-inventory="${row.id}">${t("action.edit")}</button>
        <button type="button" class="compactButton dangerButton" data-delete-inventory="${row.id}" data-delete-inventory-name="${escapeHtml(row.sku)}">${t("action.delete")}</button>
      </td>
    </tr>
  `);
  renderRows("openingLotRows", openingLots.rows, (row) => `
    <tr>
      <td>${text(row.purchase_date)}</td>
      <td>${text(row.sku)}</td>
      <td>${text(row.product_name)}</td>
      <td class="num">${row.quantity_received}</td>
      <td class="num">${money(row.unit_cost, row.currency)}</td>
      <td>${text(row.notes)}</td>
      <td><button type="button" class="compactButton dangerButton" data-delete-opening-lot="${row.id}">${t("action.delete")}</button></td>
    </tr>
  `);
  renderBundleCandidateOptions();
  renderBundleRecipes();
}

async function loadFxRates() {
  const data = await requestJson("/settings/fx-rates");
  renderRows("fxRates", data.rows, (row) => `
    <tr>
      <td>${row.currency}</td>
      <td class="num">${row.rate_to_eur}</td>
      <td>${row.effective_date}</td>
    </tr>
  `);
  const form = document.getElementById("ecbSyncForm");
  if (form) {
    const start = form.elements.namedItem("start_date");
    const end = form.elements.namedItem("end_date");
    if (!start.value) start.value = state.startDate || isoDate(new Date(new Date().getFullYear(), 0, 1));
    if (!end.value) end.value = state.endDate || isoDate(new Date());
  }
}

async function loadLandedCostSettings() {
  const data = await requestJson("/settings/landed-cost");
  const select = document.querySelector('#landedCostForm select[name="allocation_method"]');
  if (select) {
    select.value = data.allocation_method;
  }
}

async function loadFulfillmentCostSettings() {
  const data = await requestJson("/settings/fulfillment-costs");
  const form = document.getElementById("fulfillmentCostForm");
  if (!form) return;
  [
    "fba_prep_per_unit",
    "fba_storage_per_unit",
    "fbm_prep_per_unit",
    "fbm_packaging_per_unit",
    "fbm_outbound_per_unit",
    "fbm_storage_per_unit",
  ].forEach((field) => {
    const input = form.elements.namedItem(field);
    if (input) input.value = data[field];
  });
}

async function loadSupplierCatalogStats() {
  const data = await requestJson("/integrations/oa-pipeline/catalog");
  document.getElementById("catalogItems").textContent = data.items;
  document.getElementById("catalogWithEan").textContent = data.with_ean;
  document.getElementById("catalogLastSync").textContent = data.last_synced_at
    ? new Date(data.last_synced_at).toLocaleString(localeByLanguage[state.language] || "en-US")
    : "-";
}

async function loadAmazonConnector() {
  const [status, imports, returnImports] = await Promise.all([
    requestJson("/integrations/amazon-sp-api/status"),
    requestJson("/integrations/amazon-sp-api/orders/imports"),
    requestJson("/integrations/amazon-sp-api/returns/imports"),
  ]);
  document.getElementById("amazonConnectorTotals").innerHTML = `
    <div class="kpi">
      <span>${t("table.status")}</span>
      <strong>${status.configured ? "Configured" : "Manual"}</strong>
    </div>
    <div class="kpi">
      <span>${t("table.type")}</span>
      <strong>${status.phase_1_report_type}</strong>
    </div>
    <div class="kpi">
      <span>${t("table.rows")}</span>
      <strong>${imports.rows.length} + ${returnImports.rows.length}</strong>
    </div>
  `;
  renderRows("amazonOrderImports", imports.rows, (row) => `
    <tr>
      <td>${row.import_id}</td>
      <td>${text(row.marketplace)}</td>
      <td class="num">${row.row_count}</td>
      <td class="num">${row.fba_quantity}</td>
      <td class="num">${row.fbm_quantity}</td>
      <td>${text(row.report_period_start)} - ${text(row.report_period_end)}</td>
      <td>${text(row.filename)}</td>
    </tr>
  `);
  renderRows("amazonReturnImports", returnImports.rows, (row) => `
    <tr>
      <td>${row.import_id}</td>
      <td>${text(row.marketplace)}</td>
      <td class="num">${row.row_count}</td>
      <td>${text(row.report_period_start)} - ${text(row.report_period_end)}</td>
      <td>${text(row.filename)}</td>
    </tr>
  `);
  setStatus("amazonConnectorStatus", status.configured ? "status.ready" : status.missing_settings.join(", "), !status.configured, status.configured);
}

async function loadGenericImports() {
  const data = await requestJson("/imports/report-preview");
  renderRows("genericImports", data.rows, (row) => `
    <tr>
      <td>${row.import_id}</td>
      <td>${reportTypeLabel(row.report_type)}</td>
      <td class="num">${row.row_count}</td>
      <td>${row.filename}</td>
      <td>
        <button
          type="button"
          class="compactButton dangerButton"
          data-delete-generic-import="${row.import_id}"
          data-delete-generic-import-name="${escapeHtml(row.filename)}"
        >${t("action.delete")}</button>
      </td>
    </tr>
  `);
}

function reportTypeLabel(reportType) {
  const keyByType = {
    customer_returns: "report.customerReturns",
    reimbursements: "report.reimbursements",
    service_fees: "report.serviceFees",
  };
  return t(keyByType[reportType] || reportType);
}

function costMatchStatusLabel(status) {
  if (status === "matched") return t("status.matched");
  if (status === "missing_cost") return t("status.missingCost");
  return status;
}

function profitabilityStatusLabel(status) {
  if (status === "profitable") return t("status.profitable");
  if (status === "loss") return t("status.loss");
  if (status === "breakeven") return t("status.breakeven");
  if (status === "unknown") return t("status.unknown");
  return text(status);
}

function paymentCategoryLabel(category) {
  const keys = {
    order: "paymentCategory.order",
    refund: "paymentCategory.refund",
    fba_fee: "paymentCategory.fbaFee",
    return_fee: "paymentCategory.returnFee",
    service_fee: "paymentCategory.serviceFee",
    transfer: "paymentCategory.transfer",
    other: "paymentCategory.other",
    unknown: "paymentCategory.unknown",
  };
  return keys[category] ? t(keys[category]) : category;
}

function vatStatusLabel(status) {
  const keys = {
    vat_included: "vat.included",
    no_vat: "vat.none",
    vat_unknown: "vat.unknown",
  };
  return keys[status] ? t(keys[status]) : text(status);
}

function renderInvoicePreview(preview) {
  const target = document.getElementById("invoicePreview");
  const errors = preview.validation_errors || [];
  const unknownHeaders = preview.unknown_headers || [];
  const mappingEntries = Object.entries(preview.mapping || {});
  const rows = preview.normalized_sample_rows || [];
  target.classList.remove("empty");
  target.innerHTML = `
    <div class="previewHeader">
      <div>
        <strong>${t("preview.previewReady")}</strong>
        <span>${escapeHtml(preview.filename)}</span>
      </div>
      <span class="previewBadge ${preview.can_commit ? "ok" : "bad"}">${preview.can_commit ? t("status.ready") : t("preview.needsReview")}</span>
    </div>
    <div class="previewFacts">
      <div><span>${t("field.supplier")}</span><strong>${escapeHtml(preview.supplier_name)}</strong></div>
      <div><span>${t("preview.invoice")}</span><strong>${escapeHtml(preview.invoice_number)}</strong></div>
      <div><span>${t("field.invoiceDate")}</span><strong>${escapeHtml(preview.invoice_date)}</strong></div>
      <div><span>${t("field.currency")}</span><strong>${escapeHtml(preview.currency)}</strong></div>
      <div><span>${t("table.vatStatus")}</span><strong>${vatStatusLabel(preview.vat_status)}</strong></div>
      <div><span>${t("preview.lines")}</span><strong>${preview.parsed_row_count}/${preview.row_count}</strong></div>
      <div><span>${t("preview.quantity")}</span><strong>${preview.totals.quantity}</strong></div>
      <div><span>${t("preview.products")}</span><strong>${money(preview.totals.product_subtotal_amount, preview.currency)}</strong></div>
      <div><span>${t("preview.expenses")}</span><strong>${money(preview.totals.expense_subtotal_amount, preview.currency)}</strong></div>
      <div><span>${t("table.vatAmount")}</span><strong>${money(preview.totals.vat_amount, preview.currency)}</strong></div>
      <div><span>${t("preview.total")}</span><strong>${money(preview.totals.total_amount, preview.currency)}</strong></div>
    </div>
    <div class="previewTableWrap">
      <table>
        <thead>
          <tr>
            <th>${t("table.sku")}</th>
            <th>${t("table.lineType")}</th>
            <th>EAN</th>
            <th>${t("table.product")}</th>
            <th>${t("table.quantity")}</th>
            <th>${t("table.cost")}</th>
            <th>${t("table.subtotal")}</th>
            <th>${t("table.vat")}</th>
            <th>${t("table.total")}</th>
          </tr>
        </thead>
        <tbody>
          ${rows.length ? rows.map((row) => `
            <tr>
              <td>${escapeHtml(row.sku || row.supplier_sku)}</td>
              <td>${escapeHtml(lineTypeLabel(row.line_type))}</td>
              <td>${escapeHtml(row.ean)}</td>
              <td>${escapeHtml(row.product_name)}</td>
              <td class="num">${text(row.quantity)}</td>
              <td class="num">${row.unit_cost === null || row.unit_cost === undefined ? "-" : money(row.unit_cost, preview.currency)}</td>
              <td class="num">${row.line_net_amount === null || row.line_net_amount === undefined ? "-" : money(row.line_net_amount, preview.currency)}</td>
              <td class="num">${row.vat_amount === null || row.vat_amount === undefined ? "-" : money(row.vat_amount, preview.currency)}</td>
              <td class="num">${row.line_gross_amount === null || row.line_gross_amount === undefined ? "-" : money(row.line_gross_amount, preview.currency)}</td>
            </tr>
          `).join("") : `<tr><td class="muted" colspan="9">${t("message.noData")}</td></tr>`}
        </tbody>
      </table>
    </div>
    <div class="previewIssues ${errors.length || unknownHeaders.length ? "" : "ok"}">
      <strong>${errors.length || unknownHeaders.length ? t("preview.validationErrors") : t("preview.noIssues")}</strong>
      ${errors.length ? `<ul>${errors.map((error) => `<li>${escapeHtml(error)}</li>`).join("")}</ul>` : ""}
      ${unknownHeaders.length ? `<p>${t("preview.unknownHeaders")}: ${unknownHeaders.map(escapeHtml).join(", ")}</p>` : ""}
    </div>
    <details class="debugDetails">
      <summary>${t("preview.detectedFields")}</summary>
      <dl>
        ${mappingEntries.map(([key, value]) => `<div><dt>${escapeHtml(key)}</dt><dd>${escapeHtml(value)}</dd></div>`).join("")}
      </dl>
    </details>
  `;
}

function renderAmazonOrdersPreview(preview) {
  const target = document.getElementById("amazonOrdersPreview");
  target.classList.remove("empty");
  const errors = preview.validation_errors || [];
  target.innerHTML = `
    <div class="previewHeader">
      <div>
        <strong>${t("preview.previewReady")}</strong>
        <span>${escapeHtml(preview.filename)}</span>
      </div>
      <span class="previewBadge ${preview.can_commit ? "ok" : "bad"}">${preview.can_commit ? t("status.ready") : t("preview.needsReview")}</span>
    </div>
    <div class="previewFacts">
      <div><span>${t("field.marketplace")}</span><strong>${escapeHtml(preview.marketplace)}</strong></div>
      <div><span>${t("table.rows")}</span><strong>${preview.row_count}</strong></div>
      <div><span>${t("preview.quantity")}</span><strong>${preview.totals.quantity}</strong></div>
      <div><span>FBA</span><strong>${preview.totals.fba_quantity}</strong></div>
      <div><span>FBM</span><strong>${preview.totals.fbm_quantity}</strong></div>
    </div>
    <div class="previewIssues ${errors.length || preview.missing_fields.length ? "" : "ok"}">
      <strong>${errors.length || preview.missing_fields.length ? t("preview.validationErrors") : t("preview.noIssues")}</strong>
      ${preview.missing_fields.length ? `<p>${preview.missing_fields.map(escapeHtml).join(", ")}</p>` : ""}
      ${errors.length ? `<ul>${errors.map((error) => `<li>${escapeHtml(error)}</li>`).join("")}</ul>` : ""}
    </div>
  `;
}

function renderAmazonOrdersSyncResult(result) {
  const target = document.getElementById("amazonOrdersPreview");
  target.classList.remove("empty");
  const reportIds = result.report_ids?.length ? result.report_ids.join(", ") : result.report_id;
  const importIds = result.import_ids?.length ? result.import_ids.join(", ") : text(result.import_id);
  target.innerHTML = `
    <div class="previewHeader">
      <div>
        <strong>${result.status === "duplicate" ? t("status.duplicate") : t("status.imported")}</strong>
        <span>${escapeHtml(result.filename || "-")}</span>
      </div>
      <span class="previewBadge ok">${escapeHtml(result.processing_status || result.status)}</span>
    </div>
    <div class="previewFacts">
      <div><span>Reports</span><strong>${result.report_ids?.length || 1}</strong></div>
      <div><span>Report ID</span><strong>${escapeHtml(reportIds || "-")}</strong></div>
      <div><span>${t("table.id")}</span><strong>${escapeHtml(importIds || "-")}</strong></div>
      <div><span>${t("table.rows")}</span><strong>${result.row_count}</strong></div>
      <div><span>FBA</span><strong>${result.fba_quantity}</strong></div>
      <div><span>FBM</span><strong>${result.fbm_quantity}</strong></div>
    </div>
  `;
}

async function loadCashflow() {
  const data = await requestJson(`/reports/monthly-cashflow${reportQueryParams()}`);
  renderDashboardCards(data);
  const totals = document.getElementById("currencyTotals");
  totals.innerHTML = `
    <div class="kpi">
      <span>${t("table.generalTotalEur")}</span>
      <strong>${money(data.general_total_eur.total_amount_eur, "EUR")}</strong>
    </div>
  ` + data.totals_by_currency.map((row) => `
    <div class="kpi">
      <span>${t("table.marketplaceCurrencyTotal", { currency: row.currency })}</span>
      <strong>${money(row.total_amount, row.currency)}</strong>
    </div>
  `).join("");

  renderRows("cashflowRows", data.rows, (row) => `
    <tr>
      <td>${row.month}</td>
      <td>${row.marketplace}</td>
      <td>${row.currency}</td>
      <td class="num">${row.fx_rate_to_eur}</td>
      <td>${row.transaction_type}</td>
      <td class="num">${row.rows}</td>
      <td class="num">${money(row.product_charges, row.currency)}</td>
      <td class="num">${money(row.promotional_rebates, row.currency)}</td>
      <td class="num">${money(row.amazon_fees, row.currency)}</td>
      <td class="num">${money(row.other_amount, row.currency)}</td>
      <td class="num">${money(row.total_amount, row.currency)}</td>
      <td class="num">${money(row.total_amount_eur, "EUR")}</td>
    </tr>
  `);
}

async function loadAmazonPnl() {
  const data = await requestJson(`/reports/amazon-pnl${reportQueryParams()}`);
  const summary = data.summary;
  state.amazonPnlSummary = summary;
  updateDashboardPnl();
  const target = document.getElementById("amazonPnlTotals");
  if (target) {
    target.innerHTML = `
      <div class="kpi">
        <span>${t("table.grossSales")}</span>
        <strong>${money(summary.gross_sales_eur, "EUR")}</strong>
      </div>
      <div class="kpi">
        <span>${t("table.refunds")}</span>
        <strong>${money(summary.refunds_eur, "EUR")}</strong>
      </div>
      <div class="kpi">
        <span>${t("table.fees")}</span>
        <strong>${money(summary.amazon_fees_eur + summary.service_other_fees_eur, "EUR")}</strong>
      </div>
      <div class="kpi">
        <span>${t("table.amazonOperatingResult")}</span>
        <strong>${money(summary.amazon_operating_result_eur, "EUR")}</strong>
      </div>
      <div class="kpi">
        <span>${t("table.unitsSold")}</span>
        <strong>${summary.units_sold}</strong>
      </div>
      <div class="kpi">
        <span>${t("table.transfers")}</span>
        <strong>${money(summary.transfers_eur, "EUR")}</strong>
      </div>
    `;
  }
  renderRows("pnlRows", data.rows, (row) => `
    <tr>
      <td>${text(row.transaction_type)}</td>
      <td>${paymentCategoryLabel(row.category)}</td>
      <td>${text(row.fulfillment_channel)}</td>
      <td class="num">${row.rows}</td>
      <td class="num">${row.units}</td>
      <td class="num">${money(row.product_charges_eur, "EUR")}</td>
      <td class="num">${money(row.amazon_fees_eur, "EUR")}</td>
      <td class="num">${money(row.other_amount_eur, "EUR")}</td>
      <td class="num">${money(row.total_amount_eur, "EUR")}</td>
    </tr>
  `);
}

function updateDashboardPnl() {
  const summary = state.amazonPnlSummary;
  if (!summary) return;
  const sales = document.getElementById("dashboardSales");
  const ordersUnits = document.getElementById("dashboardOrdersUnits");
  const refunds = document.getElementById("dashboardPnlRefunds");
  const estimatedPayout = document.getElementById("dashboardEstimatedPayout");
  if (sales) sales.textContent = money(summary.gross_sales_eur, "EUR");
  if (ordersUnits) ordersUnits.textContent = `${summary.order_rows} / ${summary.units_sold}`;
  if (refunds) refunds.textContent = `${summary.units_refunded} (${money(summary.refunds_eur, "EUR")})`;
  if (estimatedPayout) estimatedPayout.textContent = money(summary.amazon_operating_result_eur, "EUR");
}

async function loadDataQuality() {
  const data = await requestJson(`/reports/data-quality${reportQueryParams()}`);
  const summary = data.summary;
  state.dataQualitySummary = summary;
  const target = document.getElementById("dataQualityTotals");
  if (target) {
    target.innerHTML = `
      <div class="kpi">
        <span>${t("table.paymentRows")}</span>
        <strong>${summary.payment_rows}</strong>
      </div>
      <div class="kpi">
        <span>${t("table.sku")}</span>
        <strong>${summary.rows_with_sku}/${summary.payment_rows}</strong>
      </div>
      <div class="kpi">
        <span>${t("table.costCoverage")}</span>
        <strong>${summary.sold_skus - summary.missing_cost_skus}/${summary.sold_skus}</strong>
      </div>
      <div class="kpi">
        <span>${t("table.unknownTypes")}</span>
        <strong>${summary.unknown_transaction_types}</strong>
      </div>
      <div class="kpi">
        <span>${t("table.orderMatch")}</span>
        <strong>${summary.matched_order_groups}/${summary.order_groups}${summary.order_match_percent === null ? "" : ` (${summary.order_match_percent}%)`}</strong>
      </div>
      <div class="kpi">
        <span>${t("table.units")}</span>
        <strong>${summary.matched_order_units}/${summary.matched_order_units + summary.unmatched_order_units}</strong>
      </div>
      <div class="kpi">
        <span>${t("table.refundMatch")}</span>
        <strong>${summary.matched_refund_groups}/${summary.refund_groups}</strong>
      </div>
      <div class="kpi">
        <span>${t("table.returnFeeMatch")}</span>
        <strong>${summary.matched_return_fee_groups}/${summary.return_fee_groups}${summary.ambiguous_return_fee_groups ? ` · ${summary.ambiguous_return_fee_groups} ${t("status.ambiguous")}` : ""}</strong>
      </div>
    `;
  }
  const reconciliationStatusLabel = (status) => ({
    matched: t("status.matched"),
    unmatched: t("status.unmatched"),
    quantity_mismatch: t("status.quantityMismatch"),
    ambiguous: t("status.ambiguous"),
    refund_pending: t("status.refundPending"),
    return_fee_pending: t("status.returnFeePending"),
  }[status] || status);
  renderRows("reconciliationRows", data.reconciliation_rows, (row) => `
    <tr>
      <td>${reconciliationStatusLabel(row.status)}</td>
      <td>${paymentCategoryLabel(row.category)}</td>
      <td>${text(row.external_transaction_id)}</td>
      <td>${text(row.sku)}</td>
      <td>${text(row.linked_sku)}</td>
      <td class="num">${row.payment_units}</td>
      <td class="num">${row.order_units === null ? "-" : row.order_units}</td>
      <td class="num">${money(row.amount_eur, "EUR")}</td>
    </tr>
  `);
  renderRows("missingCostRows", data.missing_costs, (row) => `
    <tr>
      <td>${text(row.sku)}</td>
      <td>${text(row.product_details)}</td>
      <td class="num">${row.units_estimated}</td>
      <td class="num">${money(row.revenue_eur, "EUR")}</td>
      <td class="num">${row.average_selling_price_eur === null ? "-" : money(row.average_selling_price_eur, "EUR")}</td>
    </tr>
  `);
}

function renderDashboardCards(data) {
  const cards = document.getElementById("dashboardCards");
  if (!cards) return;
  const general = data.general_total_eur;
  const rows = data.rows || [];
  const marketRows = data.totals_by_currency || [];
  const totalRows = rows.reduce((sum, row) => sum + row.rows, 0);
  const totalFees = rows.reduce((sum, row) => sum + row.amazon_fees_eur, 0);
  const totalProduct = rows.reduce((sum, row) => sum + row.product_charges_eur, 0);
  const primaryCurrency = marketRows[0];
  cards.innerHTML = `
    <article class="metricTile">
      <div class="metricHead">
        <strong>${t("section.amazonPnl")}</strong>
        <span>${t("table.sales")}</span>
      </div>
      <div class="metricBody">
        <div class="wideMetric"><span>${t("table.sales")}</span><strong id="dashboardSales">${money(totalProduct, "EUR")}</strong></div>
        <div><span>${t("table.ordersUnits")}</span><strong id="dashboardOrdersUnits">${general.rows} / -</strong></div>
        <div><span>${t("table.refunds")}</span><strong id="dashboardPnlRefunds">-</strong></div>
        <div><span>${t("table.fees")}</span><strong>${money(totalFees, "EUR")}</strong></div>
        <div><span>${t("table.estPayout")}</span><strong id="dashboardEstimatedPayout">${money(general.total_amount_eur, "EUR")}</strong></div>
      </div>
    </article>
    <article class="metricTile">
      <div class="metricHead">
        <strong>${t("table.product")}</strong>
        <span>${t("table.revenueEur")}</span>
      </div>
      <div class="metricBody">
        <div class="wideMetric"><span>${t("table.revenueEur")}</span><strong>${money(totalProduct, "EUR")}</strong></div>
        <div><span>${t("table.rows")}</span><strong>${totalRows}</strong></div>
        <div><span>${t("table.promo")}</span><strong>${money(rows.reduce((sum, row) => sum + row.promotional_rebates_eur, 0), "EUR")}</strong></div>
      </div>
    </article>
    <article class="metricTile">
      <div class="metricHead">
        <strong>${t("table.market")}</strong>
        <span>${primaryCurrency ? primaryCurrency.currency : "EUR"}</span>
      </div>
      <div class="metricBody">
        <div class="wideMetric"><span>${primaryCurrency ? t("table.marketplaceCurrencyTotal", { currency: primaryCurrency.currency }) : t("message.noData")}</span><strong>${primaryCurrency ? money(primaryCurrency.total_amount, primaryCurrency.currency) : "-"}</strong></div>
        <div><span>${t("table.rows")}</span><strong>${primaryCurrency ? primaryCurrency.rows : 0}</strong></div>
        <div><span>${t("field.currency")}</span><strong>${primaryCurrency ? primaryCurrency.currency : "-"}</strong></div>
      </div>
    </article>
    <article class="metricTile">
      <div class="metricHead">
        <strong>${t("section.purchaseInvoices")}</strong>
        <span>${t("table.total")}</span>
      </div>
      <div class="metricBody">
        <div class="wideMetric"><span>${t("table.subtotal")}</span><strong id="dashboardPurchaseSubtotal">-</strong></div>
        <div><span>${t("table.quantity")}</span><strong id="dashboardPurchaseQty">-</strong></div>
        <div><span>${t("table.rows")}</span><strong id="dashboardPurchaseRows">-</strong></div>
      </div>
    </article>
    <article class="metricTile">
      <div class="metricHead">
        <strong>${t("section.productProfitability")}</strong>
        <span>${t("table.netProfit")}</span>
      </div>
      <div class="metricBody metricBodyDense">
        <div class="wideMetric"><span>${t("table.netProfit")}</span><strong id="dashboardNetProfit">-</strong></div>
        <div><span>${t("table.grossProfit")}</span><strong id="dashboardGrossProfit">-</strong></div>
        <div><span>${t("table.refunds")}</span><strong id="dashboardRefunds">-</strong></div>
        <div><span>${t("table.amazonFees")}</span><strong id="dashboardAmazonFees">-</strong></div>
        <div><span>${t("table.netMargin")}</span><strong id="dashboardNetMargin">-</strong></div>
        <div><span>${t("table.netRoi")}</span><strong id="dashboardNetRoi">-</strong></div>
        <div><span>${t("table.costCoverage")}</span><strong id="dashboardCoverage">-</strong></div>
        <div><span>${t("status.profitable")}</span><strong id="dashboardProfitableProducts">-</strong></div>
      </div>
    </article>
  `;
  updateDashboardPurchase();
  updateDashboardProfit();
}

function updateDashboardProfit() {
  const summary = state.profitSummary;
  if (!summary) return;
  const netProfit = document.getElementById("dashboardNetProfit");
  const grossProfit = document.getElementById("dashboardGrossProfit");
  const refunds = document.getElementById("dashboardRefunds");
  const amazonFees = document.getElementById("dashboardAmazonFees");
  const netMargin = document.getElementById("dashboardNetMargin");
  const netRoi = document.getElementById("dashboardNetRoi");
  const coverage = document.getElementById("dashboardCoverage");
  const profitableProducts = document.getElementById("dashboardProfitableProducts");
  if (netProfit) netProfit.textContent = money(summary.net_profit_eur, "EUR");
  if (grossProfit) grossProfit.textContent = money(summary.gross_profit_eur, "EUR");
  if (refunds) refunds.textContent = money(summary.refunds_eur, "EUR");
  if (amazonFees) amazonFees.textContent = money(summary.amazon_fees_eur + summary.other_amount_eur, "EUR");
  if (netMargin) netMargin.textContent = summary.net_margin_percent === null ? "-" : `${summary.net_margin_percent}%`;
  if (netRoi) netRoi.textContent = summary.net_roi_percent === null ? "-" : `${summary.net_roi_percent}%`;
  if (coverage) coverage.textContent = `${summary.matched_products}/${summary.products}`;
  if (profitableProducts) profitableProducts.textContent = summary.profitable_products;
}

async function loadProfitability() {
  const data = await requestJson(`/reports/product-profitability${reportQueryParams({ limit: 5000 })}`);
  const summary = data.summary;
  state.profitSummary = summary;
  updateDashboardProfit();
  document.getElementById("profitTotals").innerHTML = `
    <div class="kpi">
      <span>${t("table.netProfit")}</span>
      <strong>${money(summary.net_profit_eur, "EUR")}</strong>
    </div>
    <div class="kpi">
      <span>${t("table.matchedGrossProfit")}</span>
      <strong>${money(summary.gross_profit_eur, "EUR")}</strong>
    </div>
    <div class="kpi">
      <span>${t("table.refunds")}</span>
      <strong>${money(summary.refunds_eur, "EUR")}</strong>
    </div>
    <div class="kpi">
      <span>${t("table.salesVat")}</span>
      <strong>${money(summary.sales_vat_eur, "EUR")}</strong>
    </div>
    <div class="kpi">
      <span>${t("table.amazonFees")}</span>
      <strong>${money(summary.amazon_fees_eur + summary.other_amount_eur, "EUR")}</strong>
    </div>
    <div class="kpi">
      <span>${t("table.operationalCosts")}</span>
      <strong>${money(-summary.operational_cost_eur, "EUR")}</strong>
    </div>
    <div class="kpi">
      <span>${t("table.matchedCogs")}</span>
      <strong>${money(summary.cogs_eur, "EUR")}</strong>
    </div>
    <div class="kpi">
      <span>${t("table.margin")}</span>
      <strong>${summary.margin_percent === null ? "-" : `${summary.margin_percent}%`}</strong>
    </div>
    <div class="kpi">
      <span>${t("table.matchedRoi")}</span>
      <strong>${summary.roi_percent === null ? "-" : `${summary.roi_percent}%`}</strong>
    </div>
    <div class="kpi">
      <span>${t("table.netMargin")}</span>
      <strong>${summary.net_margin_percent === null ? "-" : `${summary.net_margin_percent}%`}</strong>
    </div>
    <div class="kpi">
      <span>${t("table.netRoi")}</span>
      <strong>${summary.net_roi_percent === null ? "-" : `${summary.net_roi_percent}%`}</strong>
    </div>
    <div class="kpi">
      <span>${t("table.costCoverage")}</span>
      <strong>${summary.matched_products}/${summary.products}</strong>
    </div>
    <div class="kpi">
      <span>${t("status.profitable")}</span>
      <strong>${summary.profitable_products}</strong>
    </div>
    <div class="kpi">
      <span>${t("status.loss")}</span>
      <strong>${summary.loss_products}</strong>
    </div>
    <div class="kpi">
      <span>${t("status.breakeven")}</span>
      <strong>${summary.breakeven_products}</strong>
    </div>
  `;
  const renderProfitRow = (row) => `
    <tr>
      <td class="productNameCell" title="${escapeHtml(text(row.product_details))}"><span>${text(row.product_details)}</span></td>
      <td>${renderIdentifiers(row)}</td>
      <td>${text(row.fulfillment_channel)}</td>
      <td>${row.currency}</td>
      <td class="num">${row.fx_rate_to_eur}</td>
      <td class="num">${row.units_estimated}</td>
      <td class="num">${money(row.revenue_gross_eur, "EUR")}</td>
      <td class="num">${money(row.sales_vat_eur, "EUR")}</td>
      <td class="num">${money(row.revenue_eur, "EUR")}</td>
      <td class="num">${row.average_selling_price_eur === null ? "-" : money(row.average_selling_price_eur, "EUR")}</td>
      <td class="num">${row.purchase_cost_eur === null ? "-" : money(row.purchase_cost_eur, "EUR")}</td>
      <td class="num">${row.cogs_eur === null ? "-" : money(row.cogs_eur, "EUR")}</td>
      <td class="num">${money(row.refunds_eur, "EUR")}</td>
      <td class="num">${money(row.amazon_fees_eur + row.other_amount_eur, "EUR")}</td>
      <td class="num" title="Prep ${money(row.prep_cost_eur, "EUR")} · Storage ${money(row.storage_cost_eur, "EUR")} · FBM ${money(row.fbm_logistics_cost_eur, "EUR")}">${money(-row.operational_cost_eur, "EUR")}</td>
      <td class="num">${row.gross_profit_eur === null ? "-" : money(row.gross_profit_eur, "EUR")}</td>
      <td class="num">${row.margin_percent === null ? "-" : `${row.margin_percent}%`}</td>
      <td class="num">${row.roi_percent === null ? "-" : `${row.roi_percent}%`}</td>
      <td class="num">${row.net_profit_eur === null ? "-" : money(row.net_profit_eur, "EUR")}</td>
      <td class="num">${row.net_margin_percent === null ? "-" : `${row.net_margin_percent}%`}</td>
      <td class="num">${row.net_roi_percent === null ? "-" : `${row.net_roi_percent}%`}</td>
      <td>${row.cost_match_status === "matched" ? profitabilityStatusLabel(row.profitability_status) : costMatchStatusLabel(row.cost_match_status)}</td>
    </tr>
  `;
  renderRows("profitRows", data.rows, renderProfitRow);
  renderRows("profitRowsMirror", data.rows, renderProfitRow);
}

async function refreshAll() {
  setStatus("cashflowStatus", "status.loading", false, true);
  await Promise.all([loadPayments(), loadCosts(), loadInvoices(), loadProductMappings(), loadInventory(), loadFxRates(), loadLandedCostSettings(), loadFulfillmentCostSettings(), loadSupplierCatalogStats(), loadAmazonConnector(), loadGenericImports(), loadCashflow(), loadAmazonPnl(), loadDataQuality(), loadProfitability()]);
  setStatus("paymentStatus", "status.ready", false, true);
  setStatus("costStatus", "status.ready", false, true);
  setStatus("invoiceStatus", "status.ready", false, true);
  setStatus("mappingStatus", "status.ready", false, true);
  setStatus("inventoryStatus", "status.ready", false, true);
  setStatus("fxStatus", "status.ready", false, true);
  setStatus("landedCostStatus", "status.ready", false, true);
  setStatus("fulfillmentCostStatus", "status.ready", false, true);
  setStatus("catalogStatus", "status.ready", false, true);
  setStatus("cashflowStatus", "status.loaded", false, true);
  setStatus("profitStatus", "status.loaded", false, true);
  applySearchFilter();
}

async function runRefreshAll(button = null) {
  if (button) button.disabled = true;
  try {
    await refreshAll();
  } finally {
    if (button) button.disabled = false;
  }
}

document.getElementById("mappingSuggestions").addEventListener("click", async (event) => {
  const button = event.target.closest("button[data-map-line]");
  if (!button) return;
  button.disabled = true;
  setStatus("mappingStatus", "status.saving", false, true);
  try {
    await requestJson("/product-mappings", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        invoice_line_id: Number(button.dataset.mapLine),
        amazon_product_details: decodeURIComponent(button.dataset.amazonProduct),
        confidence: Number(button.dataset.confidence),
        match_method: "operator_confirmed",
      }),
    });
    setStatus("mappingStatus", "status.saved", false, true);
    await refreshAll();
  } catch (error) {
    setStatus("mappingStatus", error.message, true);
  } finally {
    button.disabled = false;
  }
});

document.getElementById("manualMappingForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  const button = event.currentTarget.querySelector("button");
  button.disabled = true;
  setStatus("mappingStatus", "status.loading", false, true);
  try {
    await loadProductMappings();
    setStatus("mappingStatus", "status.loaded", false, true);
  } catch (error) {
    setStatus("mappingStatus", error.message, true);
  } finally {
    button.disabled = false;
  }
});

document.getElementById("manualInvoiceLines").addEventListener("click", (event) => {
  const editButton = event.target.closest("button[data-edit-invoice-product]");
  if (editButton) {
    const rowData = state.unmappedInvoiceLines.find((item) => String(item.invoice_line_id) === String(editButton.dataset.editInvoiceProduct));
    if (rowData) {
      state.selectedMappingInvoiceLineId = rowData.invoice_line_id;
      document.querySelectorAll("#manualInvoiceLines tr").forEach((item) => {
        item.classList.toggle("selectedRow", item.dataset.manualInvoiceLine === String(state.selectedMappingInvoiceLineId));
      });
      openInvoiceProductEditForm(rowData);
    }
    return;
  }

  const row = event.target.closest("tr[data-manual-invoice-line]");
  if (!row) return;
  state.selectedMappingInvoiceLineId = Number(row.dataset.manualInvoiceLine);
  document.querySelectorAll("#manualInvoiceLines tr").forEach((item) => {
    item.classList.toggle("selectedRow", item.dataset.manualInvoiceLine === String(state.selectedMappingInvoiceLineId));
  });
});

document.getElementById("invoiceProductEditForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = event.currentTarget;
  const button = form.querySelector('button[type="submit"]');
  const lineId = document.getElementById("invoiceProductEditId").value;
  if (!lineId) return;

  button.disabled = true;
  setStatus("mappingStatus", "status.saving", false, true);
  try {
    await requestJson(`/imports/purchase-invoices/lines/${lineId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        supplier_sku: document.getElementById("invoiceProductEditSupplierSku").value.trim() || null,
        sku: document.getElementById("invoiceProductEditSku").value.trim() || null,
        ean: document.getElementById("invoiceProductEditEan").value.trim() || null,
        product_name: document.getElementById("invoiceProductEditName").value.trim(),
      }),
    });
    clearInvoiceProductEditForm();
    setStatus("mappingStatus", "status.saved", false, true);
    await refreshAll();
    if (state.selectedInvoiceId) {
      await loadInvoiceLines(state.selectedInvoiceId);
    }
  } catch (error) {
    setStatus("mappingStatus", error.message, true);
  } finally {
    button.disabled = false;
  }
});

document.getElementById("cancelInvoiceProductEditButton").addEventListener("click", clearInvoiceProductEditForm);

function clearInventoryForm() {
  document.getElementById("inventoryItemId").value = "";
  document.getElementById("inventorySku").value = "";
  document.getElementById("inventoryEan").value = "";
  document.getElementById("inventoryAsin").value = "";
  document.getElementById("inventoryProductName").value = "";
  document.getElementById("inventoryMarketplace").value = "EU";
  document.getElementById("inventoryFulfillment").value = "FBA";
  document.getElementById("inventoryOnHand").value = "";
  document.getElementById("inventoryReserved").value = "0";
  document.getElementById("inventoryInbound").value = "0";
  document.getElementById("inventoryReorderPoint").value = "0";
  document.getElementById("inventoryNotes").value = "";
}

function showInventoryForm() {
  document.getElementById("inventoryForm").classList.remove("hidden");
  document.getElementById("inventorySku").focus();
}

function hideInventoryForm() {
  document.getElementById("inventoryForm").classList.add("hidden");
}

document.getElementById("inventoryForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  const button = event.currentTarget.querySelector('button[type="submit"]');
  const itemId = document.getElementById("inventoryItemId").value;
  const payload = {
    sku: document.getElementById("inventorySku").value.trim(),
    ean: document.getElementById("inventoryEan").value.trim() || null,
    asin: document.getElementById("inventoryAsin").value.trim() || null,
    product_name: document.getElementById("inventoryProductName").value.trim() || null,
    marketplace: document.getElementById("inventoryMarketplace").value,
    fulfillment_channel: document.getElementById("inventoryFulfillment").value,
    quantity_on_hand: Number(document.getElementById("inventoryOnHand").value),
    quantity_reserved: Number(document.getElementById("inventoryReserved").value),
    quantity_inbound: Number(document.getElementById("inventoryInbound").value),
    reorder_point: Number(document.getElementById("inventoryReorderPoint").value),
    notes: document.getElementById("inventoryNotes").value.trim() || null,
  };
  button.disabled = true;
  setStatus("inventoryStatus", "status.saving", false, true);
  try {
    await requestJson(itemId ? `/inventory/items/${itemId}` : "/inventory/items", {
      method: itemId ? "PUT" : "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    clearInventoryForm();
    hideInventoryForm();
    await loadInventory();
    setStatus("inventoryStatus", "status.saved", false, true);
  } catch (error) {
    setStatus("inventoryStatus", error.message, true);
  } finally {
    button.disabled = false;
  }
});

document.getElementById("openingLotForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = event.currentTarget;
  const button = form.querySelector("button");
  button.disabled = true;
  try {
    const body = new FormData(form);
    await requestJson("/inventory/opening-lots", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        sku: body.get("sku"),
        ean: body.get("ean") || null,
        product_name: body.get("product_name"),
        purchase_date: body.get("purchase_date"),
        quantity_received: Number(body.get("quantity_received")),
        unit_cost: Number(body.get("unit_cost")),
        currency: body.get("currency"),
        notes: body.get("notes") || null,
      }),
    });
    form.reset();
    form.elements.namedItem("purchase_date").value = state.startDate || isoDate(new Date());
    await Promise.all([loadInventory(), loadProfitability()]);
  } catch (error) {
    setStatus("inventoryStatus", error.message, true);
  } finally {
    button.disabled = false;
  }
});

document.getElementById("openingLotRows").addEventListener("click", async (event) => {
  const button = event.target.closest("button[data-delete-opening-lot]");
  if (!button) return;
  if (!window.confirm(t("message.confirmDeleteOpeningLot"))) return;
  button.disabled = true;
  try {
    await requestJson(`/inventory/opening-lots/${button.dataset.deleteOpeningLot}`, {
      method: "DELETE",
    });
    await Promise.all([loadInventory(), loadProfitability()]);
  } catch (error) {
    setStatus("inventoryStatus", error.message, true);
  }
});

document.getElementById("bundleComponentForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = event.currentTarget;
  const button = form.querySelector("button");
  const body = new FormData(form);
  const componentSku = String(body.get("component_sku") || "").trim();
  const componentQuantity = Number(body.get("component_quantity"));
  const existing = state.bundleDraft.find((component) => component.component_sku === componentSku);
  if (existing) {
    existing.component_quantity = componentQuantity;
  } else {
    state.bundleDraft.push({
      component_sku: componentSku,
      component_quantity: componentQuantity,
    });
  }
  state.bundleDraftDirty = true;
  form.elements.namedItem("component_sku").value = "";
  form.elements.namedItem("component_quantity").value = "1";
  renderBundleRecipes();
  button.disabled = false;
  form.elements.namedItem("component_sku").focus();
});

document.getElementById("bundleRecipeCards").addEventListener("click", (event) => {
  if (event.target.closest("[data-start-bundle-recipe]")) {
    startBundleRecipe();
    return;
  }
  const card = event.target.closest("[data-select-bundle]");
  if (!card) return;
  state.activeBundleSku = card.dataset.selectBundle;
  state.bundleDraftOriginalSku = null;
  renderBundleRecipes();
  document.querySelector('#bundleComponentForm input[name="component_sku"]').focus();
});

document.querySelector('#bundleComponentForm input[name="bundle_sku"]').addEventListener("input", (event) => {
  state.bundleDraftDirty = true;
  renderBundleSkuSuggestions(event.currentTarget.value);
  const candidate = state.bundleCandidates.bundles.find((row) => row.sku === event.currentTarget.value.trim());
  if (candidate) {
    const nameInput = event.currentTarget.form.elements.namedItem("bundle_name");
    if (nameInput && !nameInput.value.trim()) nameInput.value = candidate.product_name || "";
  }
  renderBundleRecipes();
});

document.querySelector('#bundleComponentForm input[name="bundle_name"]').addEventListener("input", () => {
  state.bundleDraftDirty = true;
  renderBundleRecipes();
});

document.getElementById("bundleSkuSuggestions").addEventListener("click", (event) => {
  const option = event.target.closest("[data-bundle-suggestion]");
  if (!option) return;
  const form = document.getElementById("bundleComponentForm");
  const candidate = state.bundleCandidates.bundles.find((row) => row.sku === option.dataset.bundleSuggestion);
  form.elements.namedItem("bundle_sku").value = candidate.sku;
  form.elements.namedItem("bundle_name").value = candidate.product_name || "";
  state.bundleDraftDirty = true;
  renderBundleSkuSuggestions("");
  renderBundleRecipes();
  form.elements.namedItem("component_sku").focus();
});

document.getElementById("activeRecipeComponents").addEventListener("click", (event) => {
  const button = event.target.closest("button[data-remove-draft-component]");
  if (!button) return;
  state.bundleDraft.splice(Number(button.dataset.removeDraftComponent), 1);
  state.bundleDraftDirty = true;
  renderBundleRecipes();
});

document.getElementById("saveBundleRecipeButton").addEventListener("click", async (event) => {
  const button = event.currentTarget;
  const form = document.getElementById("bundleComponentForm");
  const bundleSkuInput = form.elements.namedItem("bundle_sku");
  if (!bundleSkuInput.value.trim()) {
    bundleSkuInput.reportValidity();
    bundleSkuInput.focus();
    return;
  }
  if (!state.bundleDraft.length) return;
  button.disabled = true;
  try {
    const bundleSku = form.elements.namedItem("bundle_sku").value.trim();
    await requestJson("/inventory/bundle-recipes", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        bundle_sku: bundleSku,
        bundle_name: form.elements.namedItem("bundle_name").value.trim() || null,
        original_bundle_sku: state.bundleDraftOriginalSku,
        components: state.bundleDraft,
      }),
    });
    state.activeBundleSku = bundleSku;
    state.bundleDraftOriginalSku = null;
    state.bundleDraftDirty = false;
    await Promise.all([loadInventory(), loadProfitability()]);
  } catch (error) {
    setStatus("inventoryStatus", error.message, true);
  } finally {
    button.disabled = false;
  }
});

document.getElementById("addInventoryButton").addEventListener("click", () => {
  clearInventoryForm();
  showInventoryForm();
});

document.getElementById("clearInventoryButton").addEventListener("click", () => {
  clearInventoryForm();
  hideInventoryForm();
});

document.getElementById("syncInventoryButton").addEventListener("click", async () => {
  const button = document.getElementById("syncInventoryButton");
  button.disabled = true;
  setStatus("inventoryStatus", "status.loading", false, true);
  try {
    await requestJson("/inventory/sync-from-invoices", { method: "POST" });
    await loadInventory();
    setStatus("inventoryStatus", "status.loaded", false, true);
  } catch (error) {
    setStatus("inventoryStatus", error.message, true);
  } finally {
    button.disabled = false;
  }
});

document.getElementById("inventoryRows").addEventListener("click", async (event) => {
  const editButton = event.target.closest("button[data-edit-inventory]");
  if (editButton) {
    const row = state.inventoryRows.find((item) => String(item.id) === String(editButton.dataset.editInventory));
    if (!row) return;
    document.getElementById("inventoryItemId").value = row.id;
    document.getElementById("inventorySku").value = row.sku || "";
    document.getElementById("inventoryEan").value = row.ean || "";
    document.getElementById("inventoryAsin").value = row.asin || "";
    document.getElementById("inventoryProductName").value = row.product_name || "";
    document.getElementById("inventoryMarketplace").value = row.marketplace || "EU";
    document.getElementById("inventoryFulfillment").value = row.fulfillment_channel || "FBA";
    document.getElementById("inventoryOnHand").value = row.quantity_on_hand;
    document.getElementById("inventoryReserved").value = row.quantity_reserved;
    document.getElementById("inventoryInbound").value = row.quantity_inbound;
    document.getElementById("inventoryReorderPoint").value = row.reorder_point;
    document.getElementById("inventoryNotes").value = row.notes || "";
    showInventoryForm();
    return;
  }

  const deleteButton = event.target.closest("button[data-delete-inventory]");
  if (!deleteButton) return;
  const label = deleteButton.dataset.deleteInventoryName || "";
  const confirmed = window.confirm(`${t("message.confirmDeleteInventory")}\n\n${label}`);
  if (!confirmed) return;
  deleteButton.disabled = true;
  setStatus("inventoryStatus", "status.loading", false, true);
  try {
    await requestJson(`/inventory/items/${deleteButton.dataset.deleteInventory}`, { method: "DELETE" });
    await loadInventory();
    setStatus("inventoryStatus", "status.loaded", false, true);
  } catch (error) {
    setStatus("inventoryStatus", error.message, true);
  } finally {
    deleteButton.disabled = false;
  }
});

document.getElementById("manualAmazonProducts").addEventListener("click", async (event) => {
  const button = event.target.closest("button[data-manual-map-product]");
  if (!button) return;
  if (!state.selectedMappingInvoiceLineId) {
    setStatus("mappingStatus", "message.selectInvoiceLine", true, true);
    return;
  }
  button.disabled = true;
  setStatus("mappingStatus", "status.saving", false, true);
  try {
    await requestJson("/product-mappings", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        invoice_line_id: Number(state.selectedMappingInvoiceLineId),
        amazon_product_details: decodeURIComponent(button.dataset.manualMapProduct),
        match_method: "operator_manual_search",
      }),
    });
    setStatus("mappingStatus", "status.saved", false, true);
    await refreshAll();
  } catch (error) {
    setStatus("mappingStatus", error.message, true);
  } finally {
    button.disabled = false;
  }
});

async function submitForm(form, endpoint, statusId, extra = () => {}) {
  const button = form.querySelector("button");
  button.disabled = true;
  setStatus(statusId, "status.uploading", false, true);
  try {
    const body = new FormData(form);
    extra(body);
    await requestJson(endpoint, { method: "POST", body });
    form.reset();
    setStatus(statusId, "status.imported", false, true);
    await refreshAll();
  } catch (error) {
    setStatus(statusId, error.message, true);
  } finally {
    button.disabled = false;
  }
}

document.getElementById("paymentForm").addEventListener("submit", (event) => {
  event.preventDefault();
  submitForm(event.currentTarget, "/imports/amazon-payments/commit", "paymentStatus");
});

document.getElementById("paymentImports").addEventListener("click", async (event) => {
  const deleteButton = event.target.closest("button[data-delete-payment]");
  if (deleteButton) {
    const filename = deleteButton.dataset.deletePaymentName || "";
    const confirmed = window.confirm(`${t("message.confirmDeletePayment")}\n\n${filename}`);
    if (!confirmed) return;

    deleteButton.disabled = true;
    setStatus("paymentStatus", "status.loading", false, true);
    try {
      await requestJson(`/imports/amazon-payments/${deleteButton.dataset.deletePayment}`, {
        method: "DELETE",
      });
      if (String(state.selectedPaymentId) === String(deleteButton.dataset.deletePayment)) {
        hidePaymentLines();
      }
      await refreshAll();
      setStatus("paymentStatus", "status.loaded", false, true);
    } catch (error) {
      setStatus("paymentStatus", error.message, true);
    } finally {
      deleteButton.disabled = false;
    }
    return;
  }

  const linesButton = event.target.closest("button[data-payment-lines]");
  if (!linesButton) return;
  if (String(state.selectedPaymentId) === String(linesButton.dataset.paymentLines)) {
    hidePaymentLines();
    return;
  }
  linesButton.disabled = true;
  try {
    await loadPaymentLines(linesButton.dataset.paymentLines);
  } catch (error) {
    setStatus("paymentLinesStatus", error.message, true);
  } finally {
    linesButton.disabled = false;
  }
});

document.getElementById("costForm").addEventListener("submit", (event) => {
  event.preventDefault();
  submitForm(event.currentTarget, "/imports/product-costs/commit", "costStatus");
});

function clearManualCostForm() {
  document.getElementById("manualCostId").value = "";
  document.getElementById("manualCostSku").value = "";
  document.getElementById("manualCostEan").value = "";
  document.getElementById("manualCostName").value = "";
  document.getElementById("manualCostValue").value = "";
  document.getElementById("manualCostDate").value = state.startDate || isoDate(new Date());
}

document.getElementById("manualCostForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  const button = event.currentTarget.querySelector("button");
  const costId = document.getElementById("manualCostId").value;
  const payload = {
    sku: document.getElementById("manualCostSku").value.trim(),
    ean: document.getElementById("manualCostEan").value.trim() || null,
    product_name: document.getElementById("manualCostName").value.trim() || null,
    purchase_cost: Number(document.getElementById("manualCostValue").value),
    currency: "EUR",
    effective_date: document.getElementById("manualCostDate").value,
  };
  button.disabled = true;
  setStatus("costStatus", "status.saving", false, true);
  try {
    await requestJson(costId ? `/imports/product-costs/lines/${costId}` : "/imports/product-costs/manual", {
      method: costId ? "PUT" : "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    clearManualCostForm();
    setStatus("costStatus", "status.saved", false, true);
    await refreshAll();
  } catch (error) {
    setStatus("costStatus", error.message, true);
  } finally {
    button.disabled = false;
  }
});

document.getElementById("clearManualCostButton").addEventListener("click", clearManualCostForm);

document.getElementById("costLots").addEventListener("click", (event) => {
  const button = event.target.closest("button[data-edit-cost]");
  if (!button) return;
  const row = state.productCostRows.find((item) => String(item.product_cost_id) === String(button.dataset.editCost));
  if (!row) return;
  document.getElementById("manualCostId").value = row.product_cost_id;
  document.getElementById("manualCostSku").value = row.sku || "";
  document.getElementById("manualCostEan").value = row.ean || "";
  document.getElementById("manualCostName").value = row.product_name || "";
  document.getElementById("manualCostValue").value = row.landed_unit_cost || "";
  document.getElementById("manualCostDate").value = row.purchase_date || isoDate(new Date());
});

document.getElementById("invoicePreviewButton").addEventListener("click", async () => {
  const form = document.getElementById("invoiceForm");
  const button = document.getElementById("invoicePreviewButton");
  button.disabled = true;
  setStatus("invoiceStatus", "status.loading", false, true);
  try {
    const body = new FormData(form);
    const preview = await requestJson("/imports/purchase-invoices/preview", { method: "POST", body });
    renderInvoicePreview(preview);
    setStatus("invoiceStatus", "status.loaded", false, true);
  } catch (error) {
    setStatus("invoiceStatus", error.message, true);
  } finally {
    button.disabled = false;
  }
});

document.getElementById("invoiceForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = event.currentTarget;
  const button = form.querySelector('button[type="submit"]');
  button.disabled = true;
  setStatus("invoiceStatus", "status.uploading", false, true);
  try {
    const body = new FormData(form);
    await requestJson("/imports/purchase-invoices/commit", { method: "POST", body });
    form.reset();
    const previewElement = document.getElementById("invoicePreview");
    previewElement.classList.add("empty");
    previewElement.textContent = t("status.imported");
    setStatus("invoiceStatus", "status.imported", false, true);
    await refreshAll();
  } catch (error) {
    setStatus("invoiceStatus", error.message, true);
  } finally {
    button.disabled = false;
  }
});

document.getElementById("invoiceImports").addEventListener("click", async (event) => {
  const deleteButton = event.target.closest("button[data-delete-invoice]");
  if (deleteButton) {
    const label = deleteButton.dataset.deleteInvoiceName || "";
    const confirmed = window.confirm(`${t("message.confirmDeleteInvoice")}\n\n${label}`);
    if (!confirmed) return;

    deleteButton.disabled = true;
    setStatus("invoiceStatus", "status.loading", false, true);
    try {
      await requestJson(`/imports/purchase-invoices/${deleteButton.dataset.deleteInvoice}`, {
        method: "DELETE",
      });
      if (String(state.selectedInvoiceId) === String(deleteButton.dataset.deleteInvoice)) {
        state.selectedInvoiceId = null;
        document.getElementById("invoiceLinesPanel").classList.add("hidden");
        document.getElementById("selectedInvoiceInfo").innerHTML = "";
        renderRows("invoiceLineRows", [], () => "");
      }
      await refreshAll();
      setStatus("invoiceStatus", "status.loaded", false, true);
    } catch (error) {
      setStatus("invoiceStatus", error.message, true);
    } finally {
      deleteButton.disabled = false;
    }
    return;
  }

  const button = event.target.closest("button[data-invoice-lines]");
  if (!button) return;
  if (String(state.selectedInvoiceId) === String(button.dataset.invoiceLines)) {
    hideInvoiceLines();
    return;
  }
  button.disabled = true;
  try {
    await loadInvoiceLines(button.dataset.invoiceLines);
  } catch (error) {
    setStatus("invoiceLinesStatus", error.message, true);
  } finally {
    button.disabled = false;
  }
});

document.getElementById("fxForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = event.currentTarget;
  const button = form.querySelector("button");
  button.disabled = true;
  setStatus("fxStatus", "status.saving", false, true);
  try {
    const body = new FormData(form);
    await requestJson("/settings/fx-rates", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        currency: body.get("currency"),
        rate_to_eur: Number(body.get("rate_to_eur")),
        effective_date: body.get("effective_date"),
      }),
    });
    form.reset();
    document.querySelector('#fxForm input[name="effective_date"]').valueAsDate = new Date();
    setStatus("fxStatus", "status.saved", false, true);
    await refreshAll();
  } catch (error) {
    setStatus("fxStatus", error.message, true);
  } finally {
    button.disabled = false;
  }
});

document.getElementById("ecbSyncForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = event.currentTarget;
  const button = form.querySelector("button");
  button.disabled = true;
  setStatus("fxStatus", "status.loading", false, true);
  try {
    const body = new FormData(form);
    await requestJson("/settings/fx-rates/sync-ecb", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        start_date: body.get("start_date"),
        end_date: body.get("end_date"),
        currencies: ["SEK", "GBP", "PLN"],
      }),
    });
    setStatus("fxStatus", "status.saved", false, true);
    await refreshAll();
  } catch (error) {
    setStatus("fxStatus", error.message, true);
  } finally {
    button.disabled = false;
  }
});

document.getElementById("landedCostForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = event.currentTarget;
  const button = form.querySelector("button");
  button.disabled = true;
  setStatus("landedCostStatus", "status.saving", false, true);
  try {
    const body = new FormData(form);
    await requestJson("/settings/landed-cost", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        allocation_method: body.get("allocation_method"),
      }),
    });
    setStatus("landedCostStatus", "status.saved", false, true);
    await refreshAll();
  } catch (error) {
    setStatus("landedCostStatus", error.message, true);
  } finally {
    button.disabled = false;
  }
});

document.getElementById("fulfillmentCostForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = event.currentTarget;
  const button = form.querySelector("button");
  button.disabled = true;
  setStatus("fulfillmentCostStatus", "status.saving", false, true);
  try {
    const body = new FormData(form);
    await requestJson("/settings/fulfillment-costs", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        currency: "EUR",
        fba_prep_per_unit: Number(body.get("fba_prep_per_unit")),
        fba_storage_per_unit: Number(body.get("fba_storage_per_unit")),
        fbm_prep_per_unit: Number(body.get("fbm_prep_per_unit")),
        fbm_packaging_per_unit: Number(body.get("fbm_packaging_per_unit")),
        fbm_outbound_per_unit: Number(body.get("fbm_outbound_per_unit")),
        fbm_storage_per_unit: Number(body.get("fbm_storage_per_unit")),
      }),
    });
    setStatus("fulfillmentCostStatus", "status.saved", false, true);
    await loadProfitability();
  } catch (error) {
    setStatus("fulfillmentCostStatus", error.message, true);
  } finally {
    button.disabled = false;
  }
});

document.getElementById("syncCatalogButton").addEventListener("click", async () => {
  const button = document.getElementById("syncCatalogButton");
  button.disabled = true;
  setStatus("catalogStatus", "status.loading", false, true);
  try {
    await requestJson("/integrations/oa-pipeline/catalog/sync", { method: "POST" });
    await loadSupplierCatalogStats();
    setStatus("catalogStatus", "status.loaded", false, true);
  } catch (error) {
    setStatus("catalogStatus", error.message, true);
  } finally {
    button.disabled = false;
  }
});

document.getElementById("amazonOrdersSyncForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = event.currentTarget;
  const button = form.querySelector('button[type="submit"]');
  const formData = new FormData(form);
  button.disabled = true;
  setStatus("amazonConnectorStatus", "status.loading", false, true);
  try {
    const result = await requestJson("/integrations/amazon-sp-api/orders/sync", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        marketplace: formData.get("marketplace"),
        start_date: formData.get("start_date"),
        end_date: formData.get("end_date"),
        poll_interval_seconds: 30,
        wait_timeout_seconds: 300,
      }),
    });
    renderAmazonOrdersSyncResult(result);
    await loadAmazonConnector();
    setStatus("amazonConnectorStatus", result.status === "duplicate" ? "status.duplicate" : "status.imported", false, true);
  } catch (error) {
    setStatus("amazonConnectorStatus", error.message, true);
  } finally {
    button.disabled = false;
  }
});

document.getElementById("amazonReturnsSyncButton").addEventListener("click", async () => {
  const form = document.getElementById("amazonOrdersSyncForm");
  const button = document.getElementById("amazonReturnsSyncButton");
  const formData = new FormData(form);
  if (!form.reportValidity()) return;
  button.disabled = true;
  setStatus("amazonConnectorStatus", "status.loading", false, true);
  try {
    const result = await requestJson("/integrations/amazon-sp-api/returns/sync", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        marketplace: formData.get("marketplace"),
        start_date: formData.get("start_date"),
        end_date: formData.get("end_date"),
        poll_interval_seconds: 30,
        wait_timeout_seconds: 600,
      }),
    });
    document.getElementById("amazonOrdersPreview").textContent = JSON.stringify(result, null, 2);
    await Promise.all([loadAmazonConnector(), loadDataQuality()]);
    setStatus("amazonConnectorStatus", result.status === "duplicate" ? "status.duplicate" : "status.imported", false, true);
  } catch (error) {
    setStatus("amazonConnectorStatus", error.message, true);
  } finally {
    button.disabled = false;
  }
});

document.getElementById("amazonFbaInventorySyncButton").addEventListener("click", async () => {
  const button = document.getElementById("amazonFbaInventorySyncButton");
  button.disabled = true;
  setStatus("amazonConnectorStatus", "status.loading", false, true);
  try {
    const result = await requestJson("/integrations/amazon-sp-api/inventory/sync", {
      method: "POST",
    });
    document.getElementById("amazonOrdersPreview").textContent = JSON.stringify(result, null, 2);
    await loadInventory();
    setStatus("amazonConnectorStatus", "status.imported", false, true);
  } catch (error) {
    setStatus("amazonConnectorStatus", error.message, true);
  } finally {
    button.disabled = false;
  }
});

document.getElementById("amazonOrdersPreviewButton").addEventListener("click", async () => {
  const form = document.getElementById("amazonOrdersForm");
  const button = document.getElementById("amazonOrdersPreviewButton");
  button.disabled = true;
  setStatus("amazonConnectorStatus", "status.loading", false, true);
  try {
    const body = new FormData(form);
    const preview = await requestJson("/integrations/amazon-sp-api/orders/preview", { method: "POST", body });
    renderAmazonOrdersPreview(preview);
    setStatus("amazonConnectorStatus", "status.loaded", false, true);
  } catch (error) {
    setStatus("amazonConnectorStatus", error.message, true);
  } finally {
    button.disabled = false;
  }
});

document.getElementById("amazonOrdersForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = event.currentTarget;
  const button = form.querySelector('button[type="submit"]');
  button.disabled = true;
  setStatus("amazonConnectorStatus", "status.uploading", false, true);
  try {
    const body = new FormData(form);
    await requestJson("/integrations/amazon-sp-api/orders/commit", { method: "POST", body });
    form.reset();
    document.getElementById("amazonOrdersPreview").textContent = t("status.imported");
    await loadAmazonConnector();
    setStatus("amazonConnectorStatus", "status.imported", false, true);
  } catch (error) {
    setStatus("amazonConnectorStatus", error.message, true);
  } finally {
    button.disabled = false;
  }
});

document.getElementById("genericPreviewForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = event.currentTarget;
  const button = form.querySelector("button");
  button.disabled = true;
  setStatus("genericStatus", "status.loading", false, true);
  try {
    const body = new FormData(form);
    const preview = await requestJson("/imports/report-preview", { method: "POST", body });
    const previewElement = document.getElementById("genericPreview");
    delete previewElement.dataset.i18n;
    previewElement.textContent = JSON.stringify(preview, null, 2);
    setStatus("genericStatus", "status.loaded", false, true);
  } catch (error) {
    setStatus("genericStatus", error.message, true);
  } finally {
    button.disabled = false;
  }
});

document.getElementById("genericCommitButton").addEventListener("click", async () => {
  const form = document.getElementById("genericPreviewForm");
  const button = document.getElementById("genericCommitButton");
  button.disabled = true;
  setStatus("genericStatus", "status.saving", false, true);
  try {
    const body = new FormData(form);
    await requestJson("/imports/report-preview/commit", { method: "POST", body });
    form.reset();
    const previewElement = document.getElementById("genericPreview");
    delete previewElement.dataset.i18n;
    previewElement.textContent = t("message.committedRaw");
    setStatus("genericStatus", "status.committed", false, true);
    await refreshAll();
  } catch (error) {
    setStatus("genericStatus", error.message, true);
  } finally {
    button.disabled = false;
  }
});

document.getElementById("genericImports").addEventListener("click", async (event) => {
  const button = event.target.closest("button[data-delete-generic-import]");
  if (!button) return;
  const filename = button.dataset.deleteGenericImportName || "";
  const confirmed = window.confirm(`${t("message.confirmDeleteGenericReport")}\n\n${filename}`);
  if (!confirmed) return;
  button.disabled = true;
  setStatus("genericStatus", "status.loading", false, true);
  try {
    await requestJson(`/imports/report-preview/${button.dataset.deleteGenericImport}`, {
      method: "DELETE",
    });
    await refreshAll();
    setStatus("genericStatus", "status.loaded", false, true);
  } catch (error) {
    setStatus("genericStatus", error.message, true);
  } finally {
    button.disabled = false;
  }
});

document.getElementById("refreshButton")?.addEventListener("click", () => runRefreshAll());
document.getElementById("refreshReportsButton")?.addEventListener("click", (event) => {
  runRefreshAll(event.currentTarget).catch((error) => setStatus("cashflowStatus", error.message, true));
});

document.querySelectorAll(".navItem").forEach((button) => {
  button.addEventListener("click", () => showSection(button.dataset.sectionTarget, true));
});

document.getElementById("sidebarToggle").addEventListener("click", () => {
  document.querySelector(".appShell").classList.toggle("sidebarCollapsed");
});

document.getElementById("globalSearch").addEventListener("input", applySearchFilter);

document.getElementById("periodPreset").addEventListener("change", async (event) => {
  state.periodPreset = event.currentTarget.value;
  syncPeriodControls();
  persistPeriod();
  await refreshAll();
});

document.getElementById("startDateFilter").addEventListener("change", async (event) => {
  state.periodPreset = "custom";
  state.startDate = event.currentTarget.value;
  syncPeriodControls();
  persistPeriod();
  await refreshAll();
});

document.getElementById("endDateFilter").addEventListener("change", async (event) => {
  state.periodPreset = "custom";
  state.endDate = event.currentTarget.value;
  syncPeriodControls();
  persistPeriod();
  await refreshAll();
});

document.getElementById("languageSelect").addEventListener("change", (event) => {
  state.language = event.currentTarget.value;
  localStorage.setItem("mirenelleOpsLanguage", state.language);
  applyTranslations();
  refreshAll().catch((error) => setStatus("cashflowStatus", error.message, true));
});

document.getElementById("mockCostsButton")?.addEventListener("click", async () => {
  const button = document.getElementById("mockCostsButton");
  button.disabled = true;
  setStatus("costStatus", "status.mockingCosts", false, true);
  try {
    await requestJson("/tools/mock-costs/from-transactions", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ cost_ratio: 0.45 }),
    });
    setStatus("costStatus", "status.mockCostsCreated", false, true);
    await refreshAll();
  } catch (error) {
    setStatus("costStatus", error.message, true);
  } finally {
    button.disabled = false;
  }
});

document.querySelector('#costForm input[name="effective_date"]').valueAsDate = new Date();
document.getElementById("manualCostDate").valueAsDate = new Date();
document.querySelector('#fxForm input[name="effective_date"]').valueAsDate = new Date();
document.getElementById("languageSelect").value = state.language;
syncPeriodControls();
persistPeriod();
applyTranslations();
showSection(state.activeSection, true);
refreshAll().catch((error) => setStatus("cashflowStatus", error.message, true));
