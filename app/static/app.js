const translations = {
  en: {
    "app.tagline": "Amazon accounting imports, product costs, and monthly cashflow.",
    "action.add": "Add",
    "action.commit": "Commit",
    "action.commitRaw": "Commit raw",
    "action.mockCosts": "Mock Costs",
    "action.preview": "Preview",
    "action.refresh": "Refresh",
    "action.refreshReports": "Refresh reports",
    "action.search": "Search",
    "action.save": "Save",
    "action.clear": "Clear",
    "action.edit": "Edit",
    "action.delete": "Delete",
    "action.syncOaCatalog": "Sync OA catalog",
    "action.syncInventory": "Sync stock",
    "action.useMatch": "Use",
    "action.viewLines": "Lines",
    "field.costFile": "Cost CSV/XLSX",
    "field.csvReport": "CSV report",
    "field.currency": "Currency",
    "field.effectiveDate": "Effective date",
    "field.invoiceDate": "Invoice date",
    "field.invoiceFile": "Invoice CSV/XLSX/PDF",
    "field.invoiceNumber": "Invoice number",
    "field.marketplace": "Marketplace",
    "field.rateToEur": "Rate to EUR",
    "field.reportType": "Report type",
    "field.search": "Search",
    "field.supplier": "Supplier",
    "field.supplierSku": "Supplier SKU",
    "field.productName": "Product name",
    "field.fulfillment": "Fulfillment",
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
    "message.selectInvoiceLine": "Select an invoice product first.",
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
    "section.fxRates": "FX Rates",
    "section.generalCashflow": "General Cashflow",
    "section.inventory": "Inventory",
    "section.invoiceLines": "Invoice Lines",
    "section.paymentLines": "Payment Lines",
    "section.productCosts": "Product Costs",
    "section.productMappings": "Product Mappings",
    "section.oaCatalog": "OA Catalog",
    "section.amazonPnl": "Amazon P&L",
    "section.dataQuality": "Data Quality",
    "section.productProfitability": "Product Profitability",
    "section.purchaseSummary": "Purchase Summary",
    "section.purchaseInvoices": "Purchase Invoices",
    "section.reportPreview": "Report Preview",
    "status.committed": "Committed",
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
    "status.healthy": "healthy",
    "status.lowStock": "low stock",
    "status.outOfStock": "out of stock",
    "status.ready": "Ready",
    "status.saved": "Saved",
    "status.saving": "Saving",
    "status.uploading": "Uploading",
    "table.action": "Action",
    "table.amazonProduct": "Amazon product",
    "table.avgSellingPrice": "Avg selling price",
    "table.amazonOperatingResult": "Amazon operating result",
    "table.cogsEur": "COGS EUR",
    "table.confidence": "Confidence",
    "table.cost": "Cost",
    "table.costCoverage": "Cost coverage",
    "table.costEur": "Cost EUR",
    "table.date": "Date",
    "table.effective": "Effective",
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
    "table.other": "Other",
    "table.onHand": "On hand",
    "table.paymentRows": "Payment rows",
    "table.period": "Period",
    "table.product": "Product",
    "table.productCharges": "Product charges",
    "table.promo": "Promo",
    "table.refunds": "Refunds",
    "table.reorderPoint": "Reorder point",
    "table.reserved": "Reserved",
    "table.quantity": "Quantity",
    "table.revenueEur": "Revenue EUR",
    "table.revenue": "Revenue",
    "table.roi": "ROI",
    "table.rows": "Rows",
    "table.salesCurrency": "Sales currency",
    "table.sku": "SKU",
    "table.status": "Status",
    "table.subtotal": "Subtotal",
    "table.total": "Total",
    "table.totalEur": "Total EUR",
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
    "action.commit": "Speichern",
    "action.commitRaw": "Rohdaten speichern",
    "action.mockCosts": "Preise mocken",
    "action.preview": "Vorschau",
    "action.refresh": "Aktualisieren",
    "action.refreshReports": "Reports aktualisieren",
    "action.search": "Suchen",
    "action.save": "Speichern",
    "action.clear": "Leeren",
    "action.edit": "Bearbeiten",
    "action.delete": "Löschen",
    "action.syncOaCatalog": "OA-Katalog synchronisieren",
    "action.syncInventory": "Bestand synchronisieren",
    "action.useMatch": "Nutzen",
    "action.viewLines": "Zeilen",
    "field.costFile": "Kosten CSV/XLSX",
    "field.csvReport": "CSV-Report",
    "field.currency": "Währung",
    "field.effectiveDate": "Gültig ab",
    "field.invoiceDate": "Rechnungsdatum",
    "field.invoiceFile": "Rechnung CSV/XLSX/PDF",
    "field.invoiceNumber": "Rechnungsnummer",
    "field.marketplace": "Marketplace",
    "field.rateToEur": "Kurs zu EUR",
    "field.reportType": "Reporttyp",
    "field.search": "Suchen",
    "field.supplier": "Lieferant",
    "field.supplierSku": "Lieferanten-SKU",
    "field.productName": "Produktname",
    "field.fulfillment": "Fulfillment",
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
    "message.selectInvoiceLine": "Wähle zuerst ein Rechnungsprodukt.",
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
    "section.fxRates": "Wechselkurse",
    "section.generalCashflow": "Gesamt-Cashflow",
    "section.inventory": "Bestand",
    "section.invoiceLines": "Rechnungszeilen",
    "section.paymentLines": "Zahlungszeilen",
    "section.productCosts": "Einkaufspreise",
    "section.productMappings": "Produktzuordnung",
    "section.oaCatalog": "OA-Katalog",
    "section.amazonPnl": "Amazon P&L",
    "section.dataQuality": "Datenqualität",
    "section.productProfitability": "Produktprofitabilität",
    "section.purchaseSummary": "Einkaufsübersicht",
    "section.purchaseInvoices": "Einkaufsrechnungen",
    "section.reportPreview": "Report-Vorschau",
    "status.committed": "Gespeichert",
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
    "status.healthy": "gesund",
    "status.lowStock": "niedriger Bestand",
    "status.outOfStock": "ausverkauft",
    "status.ready": "Bereit",
    "status.saved": "Gespeichert",
    "status.saving": "Speichert",
    "status.uploading": "Lädt hoch",
    "table.action": "Aktion",
    "table.amazonProduct": "Amazon-Produkt",
    "table.avgSellingPrice": "Ø Verkaufspreis",
    "table.amazonOperatingResult": "Amazon-Betriebsergebnis",
    "table.cogsEur": "Wareneinsatz EUR",
    "table.confidence": "Konfidenz",
    "table.cost": "Kosten",
    "table.costCoverage": "Kostenabdeckung",
    "table.costEur": "Kosten EUR",
    "table.date": "Datum",
    "table.effective": "Gültig",
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
    "table.other": "Sonstiges",
    "table.onHand": "Auf Lager",
    "table.paymentRows": "Zahlungszeilen",
    "table.period": "Zeitraum",
    "table.product": "Produkt",
    "table.productCharges": "Produktumsatz",
    "table.promo": "Promo",
    "table.refunds": "Erstattungen",
    "table.reorderPoint": "Meldebestand",
    "table.reserved": "Reserviert",
    "table.quantity": "Menge",
    "table.revenueEur": "Umsatz EUR",
    "table.revenue": "Umsatz",
    "table.roi": "ROI",
    "table.rows": "Zeilen",
    "table.salesCurrency": "Verkaufswährung",
    "table.sku": "SKU",
    "table.status": "Status",
    "table.subtotal": "Zwischensumme",
    "table.total": "Summe",
    "table.totalEur": "Summe EUR",
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
    "action.commit": "Зберегти",
    "action.commitRaw": "Зберегти raw",
    "action.mockCosts": "Mock цін",
    "action.preview": "Preview",
    "action.refresh": "Оновити",
    "action.refreshReports": "Оновити звіти",
    "action.search": "Пошук",
    "action.save": "Зберегти",
    "action.clear": "Очистити",
    "action.edit": "Редагувати",
    "action.delete": "Видалити",
    "action.syncOaCatalog": "Синхронізувати OA каталог",
    "action.syncInventory": "Синхронізувати залишки",
    "action.useMatch": "Застосувати",
    "action.viewLines": "Позиції",
    "field.costFile": "Файл цін CSV/XLSX",
    "field.csvReport": "CSV-звіт",
    "field.currency": "Валюта",
    "field.effectiveDate": "Дата дії",
    "field.invoiceDate": "Дата інвойсу",
    "field.invoiceFile": "Інвойс CSV/XLSX/PDF",
    "field.invoiceNumber": "Номер інвойсу",
    "field.marketplace": "Маркетплейс",
    "field.rateToEur": "Курс до EUR",
    "field.reportType": "Тип звіту",
    "field.search": "Пошук",
    "field.supplier": "Постачальник",
    "field.supplierSku": "SKU постачальника",
    "field.productName": "Назва товару",
    "field.fulfillment": "Фулфілмент",
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
    "message.selectInvoiceLine": "Спочатку обери товар з інвойсу.",
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
    "section.fxRates": "Курси валют",
    "section.generalCashflow": "Загальний cashflow",
    "section.inventory": "Товарні залишки",
    "section.invoiceLines": "Позиції інвойсу",
    "section.paymentLines": "Рядки платежу",
    "section.productCosts": "Закупівельні ціни",
    "section.productMappings": "Мапінг товарів",
    "section.oaCatalog": "OA каталог",
    "section.amazonPnl": "Amazon P&L",
    "section.dataQuality": "Якість даних",
    "section.productProfitability": "Прибутковість товарів",
    "section.purchaseSummary": "Підсумок закупівель",
    "section.purchaseInvoices": "Інвойси закупівель",
    "section.reportPreview": "Preview звіту",
    "status.committed": "Збережено",
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
    "status.healthy": "норма",
    "status.lowStock": "низький залишок",
    "status.outOfStock": "немає в наявності",
    "status.ready": "Готово",
    "status.saved": "Збережено",
    "status.saving": "Збереження",
    "status.uploading": "Завантаження",
    "table.action": "Дія",
    "table.amazonProduct": "Amazon товар",
    "table.avgSellingPrice": "Сер. ціна продажу",
    "table.amazonOperatingResult": "Операційний результат Amazon",
    "table.cogsEur": "COGS EUR",
    "table.confidence": "Впевненість",
    "table.cost": "Ціна",
    "table.costCoverage": "Покриття цін",
    "table.costEur": "Ціна EUR",
    "table.date": "Дата",
    "table.effective": "Діє з",
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
    "table.other": "Інше",
    "table.onHand": "На складі",
    "table.paymentRows": "Рядки платежів",
    "table.period": "Період",
    "table.product": "Товар",
    "table.productCharges": "Продажі товару",
    "table.promo": "Промо",
    "table.refunds": "Повернення",
    "table.reorderPoint": "Мін. залишок",
    "table.reserved": "Зарезервовано",
    "table.quantity": "Кількість",
    "table.revenueEur": "Дохід EUR",
    "table.revenue": "Дохід",
    "table.roi": "ROI",
    "table.rows": "Рядки",
    "table.salesCurrency": "Валюта продажу",
    "table.sku": "SKU",
    "table.status": "Статус",
    "table.subtotal": "Сума без ПДВ",
    "table.total": "Разом",
    "table.totalEur": "Разом EUR",
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

function updatePageTitle() {
  const title = document.getElementById("pageTitle");
  if (title) title.textContent = t(sectionTitleKey[state.activeSection] || "nav.dashboard");
}

function showSection(sectionName) {
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
  const imports = await requestJson(`/imports/product-costs${reportQueryParams()}`);
  renderRows("costImports", imports.rows, (row) => `
    <tr>
      <td>${row.import_id}</td>
      <td class="num">${row.row_count}</td>
      <td>${row.effective_date}</td>
      <td>${row.filename}</td>
      <td>
        <button
          type="button"
          class="compactButton dangerButton"
          data-delete-cost-import="${row.import_id}"
          data-delete-cost-import-name="${escapeHtml(row.filename)}"
        >${t("action.delete")}</button>
      </td>
    </tr>
  `);

  const latest = await requestJson("/reports/product-costs/latest");
  state.productCostRows = latest.rows;
  renderRows("latestCosts", latest.rows, (row) => `
    <tr>
      <td>${row.sku}</td>
      <td>${text(row.ean)}</td>
      <td>${text(row.product_name)}</td>
      <td class="num">${money(row.purchase_cost, row.currency)}</td>
      <td>${row.effective_date}</td>
      <td>
        <button type="button" class="compactButton" data-edit-cost="${row.id}">${t("action.edit")}</button>
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

function renderInventoryTotals(summary) {
  document.getElementById("inventoryTotals").innerHTML = `
    <div class="kpi">
      <span data-i18n="table.product">${t("table.product")}</span>
      <strong>${summary.products}</strong>
    </div>
    <div class="kpi">
      <span data-i18n="table.onHand">${t("table.onHand")}</span>
      <strong>${summary.total_on_hand}</strong>
    </div>
    <div class="kpi">
      <span data-i18n="table.available">${t("table.available")}</span>
      <strong>${summary.total_available}</strong>
    </div>
    <div class="kpi">
      <span data-i18n="table.inbound">${t("table.inbound")}</span>
      <strong>${summary.total_inbound}</strong>
    </div>
    <div class="kpi">
      <span data-i18n="status.lowStock">${t("status.lowStock")}</span>
      <strong>${summary.low_stock}</strong>
    </div>
    <div class="kpi">
      <span data-i18n="status.outOfStock">${t("status.outOfStock")}</span>
      <strong>${summary.out_of_stock}</strong>
    </div>
  `;
}

async function loadInventory() {
  const [summary, items] = await Promise.all([
    requestJson("/inventory/summary"),
    requestJson("/inventory/items"),
  ]);
  state.inventoryRows = items.rows;
  renderInventoryTotals(summary);
  renderRows("inventoryRows", items.rows, (row) => `
    <tr>
      <td><span class="statusPill ${row.status}">${inventoryStatusLabel(row.status)}</span></td>
      <td>${text(row.product_name)}</td>
      <td>${renderIdentifiers(row)}</td>
      <td>${text(row.marketplace)}</td>
      <td>${text(row.fulfillment_channel)}</td>
      <td class="num">${row.quantity_on_hand}</td>
      <td class="num">${row.quantity_available}</td>
      <td class="num">${row.quantity_reserved}</td>
      <td class="num">${row.quantity_inbound}</td>
      <td class="num">${row.reorder_point}</td>
      <td>${new Date(row.updated_at).toLocaleString(localeByLanguage[state.language] || "en-US")}</td>
      <td>
        <button type="button" class="compactButton" data-edit-inventory="${row.id}">${t("action.edit")}</button>
        <button type="button" class="compactButton dangerButton" data-delete-inventory="${row.id}" data-delete-inventory-name="${escapeHtml(row.sku)}">${t("action.delete")}</button>
      </td>
    </tr>
  `);
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
}

async function loadSupplierCatalogStats() {
  const data = await requestJson("/integrations/oa-pipeline/catalog");
  document.getElementById("catalogItems").textContent = data.items;
  document.getElementById("catalogWithEan").textContent = data.with_ean;
  document.getElementById("catalogLastSync").textContent = data.last_synced_at
    ? new Date(data.last_synced_at).toLocaleString(localeByLanguage[state.language] || "en-US")
    : "-";
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
      <div><span>${t("preview.lines")}</span><strong>${preview.parsed_row_count}/${preview.row_count}</strong></div>
      <div><span>${t("preview.quantity")}</span><strong>${preview.totals.quantity}</strong></div>
      <div><span>${t("preview.products")}</span><strong>${money(preview.totals.product_subtotal_amount, preview.currency)}</strong></div>
      <div><span>${t("preview.expenses")}</span><strong>${money(preview.totals.expense_subtotal_amount, preview.currency)}</strong></div>
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
            <th>VAT</th>
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
      <td class="num">${row.rows}</td>
      <td class="num">${row.units}</td>
      <td class="num">${money(row.product_charges_eur, "EUR")}</td>
      <td class="num">${money(row.amazon_fees_eur, "EUR")}</td>
      <td class="num">${money(row.other_amount_eur, "EUR")}</td>
      <td class="num">${money(row.total_amount_eur, "EUR")}</td>
    </tr>
  `);
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
    `;
  }
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
        <strong>${t("section.generalCashflow")}</strong>
        <span>${t("table.generalTotalEur")}</span>
      </div>
      <div class="metricBody">
        <div class="wideMetric"><span>${t("table.totalEur")}</span><strong>${money(general.total_amount_eur, "EUR")}</strong></div>
        <div><span>${t("table.rows")}</span><strong>${general.rows}</strong></div>
        <div><span>${t("table.fees")}</span><strong>${money(totalFees, "EUR")}</strong></div>
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
        <span>${t("table.matchedGrossProfit")}</span>
      </div>
      <div class="metricBody">
        <div class="wideMetric"><span>${t("table.grossProfit")}</span><strong id="dashboardGrossProfit">-</strong></div>
        <div><span>${t("table.margin")}</span><strong id="dashboardMargin">-</strong></div>
        <div><span>${t("table.roi")}</span><strong id="dashboardRoi">-</strong></div>
        <div><span>${t("table.costCoverage")}</span><strong id="dashboardCoverage">-</strong></div>
      </div>
    </article>
  `;
  updateDashboardPurchase();
  updateDashboardProfit();
}

function updateDashboardProfit() {
  const summary = state.profitSummary;
  if (!summary) return;
  const grossProfit = document.getElementById("dashboardGrossProfit");
  const margin = document.getElementById("dashboardMargin");
  const roi = document.getElementById("dashboardRoi");
  const coverage = document.getElementById("dashboardCoverage");
  if (grossProfit) grossProfit.textContent = money(summary.gross_profit_eur, "EUR");
  if (margin) margin.textContent = summary.margin_percent === null ? "-" : `${summary.margin_percent}%`;
  if (roi) roi.textContent = summary.roi_percent === null ? "-" : `${summary.roi_percent}%`;
  if (coverage) coverage.textContent = `${summary.matched_products}/${summary.products}`;
}

async function loadProfitability() {
  const data = await requestJson(`/reports/product-profitability${reportQueryParams({ limit: 5000 })}`);
  const summary = data.summary;
  state.profitSummary = summary;
  updateDashboardProfit();
  document.getElementById("profitTotals").innerHTML = `
    <div class="kpi">
      <span>${t("table.matchedGrossProfit")}</span>
      <strong>${money(summary.gross_profit_eur, "EUR")}</strong>
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
      <td>${text(row.product_details)}</td>
      <td>${renderIdentifiers(row)}</td>
      <td>${row.currency}</td>
      <td class="num">${row.fx_rate_to_eur}</td>
      <td class="num">${row.units_estimated}</td>
      <td class="num">${money(row.revenue_eur, "EUR")}</td>
      <td class="num">${row.average_selling_price_eur === null ? "-" : money(row.average_selling_price_eur, "EUR")}</td>
      <td class="num">${row.purchase_cost_eur === null ? "-" : money(row.purchase_cost_eur, "EUR")}</td>
      <td class="num">${row.cogs_eur === null ? "-" : money(row.cogs_eur, "EUR")}</td>
      <td class="num">${row.gross_profit_eur === null ? "-" : money(row.gross_profit_eur, "EUR")}</td>
      <td class="num">${row.margin_percent === null ? "-" : `${row.margin_percent}%`}</td>
      <td class="num">${row.roi_percent === null ? "-" : `${row.roi_percent}%`}</td>
      <td>${row.cost_match_status === "matched" ? profitabilityStatusLabel(row.profitability_status) : costMatchStatusLabel(row.cost_match_status)}</td>
    </tr>
  `;
  renderRows("profitRows", data.rows, renderProfitRow);
  renderRows("profitRowsMirror", data.rows, renderProfitRow);
}

async function refreshAll() {
  setStatus("cashflowStatus", "status.loading", false, true);
  await Promise.all([loadPayments(), loadCosts(), loadInvoices(), loadProductMappings(), loadInventory(), loadFxRates(), loadSupplierCatalogStats(), loadGenericImports(), loadCashflow(), loadAmazonPnl(), loadDataQuality(), loadProfitability()]);
  setStatus("paymentStatus", "status.ready", false, true);
  setStatus("costStatus", "status.ready", false, true);
  setStatus("invoiceStatus", "status.ready", false, true);
  setStatus("mappingStatus", "status.ready", false, true);
  setStatus("inventoryStatus", "status.ready", false, true);
  setStatus("fxStatus", "status.ready", false, true);
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

document.getElementById("clearInvoiceProductEditButton").addEventListener("click", clearInvoiceProductEditForm);

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
    await loadInventory();
    setStatus("inventoryStatus", "status.saved", false, true);
  } catch (error) {
    setStatus("inventoryStatus", error.message, true);
  } finally {
    button.disabled = false;
  }
});

document.getElementById("clearInventoryButton").addEventListener("click", clearInventoryForm);

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
    document.getElementById("inventorySku").focus();
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

document.getElementById("latestCosts").addEventListener("click", (event) => {
  const button = event.target.closest("button[data-edit-cost]");
  if (!button) return;
  const row = state.productCostRows.find((item) => String(item.id) === String(button.dataset.editCost));
  if (!row) return;
  document.getElementById("manualCostId").value = row.id;
  document.getElementById("manualCostSku").value = row.sku || "";
  document.getElementById("manualCostEan").value = row.ean || "";
  document.getElementById("manualCostName").value = row.product_name || "";
  document.getElementById("manualCostValue").value = row.purchase_cost || "";
  document.getElementById("manualCostDate").value = row.effective_date || isoDate(new Date());
});

document.getElementById("costImports").addEventListener("click", async (event) => {
  const button = event.target.closest("button[data-delete-cost-import]");
  if (!button) return;
  const filename = button.dataset.deleteCostImportName || "";
  const confirmed = window.confirm(`${t("message.confirmDeleteCostImport")}\n\n${filename}`);
  if (!confirmed) return;
  button.disabled = true;
  setStatus("costStatus", "status.loading", false, true);
  try {
    await requestJson(`/imports/product-costs/${button.dataset.deleteCostImport}`, {
      method: "DELETE",
    });
    await refreshAll();
    setStatus("costStatus", "status.loaded", false, true);
  } catch (error) {
    setStatus("costStatus", error.message, true);
  } finally {
    button.disabled = false;
  }
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
  button.addEventListener("click", () => showSection(button.dataset.sectionTarget));
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
showSection(state.activeSection);
refreshAll().catch((error) => setStatus("cashflowStatus", error.message, true));
