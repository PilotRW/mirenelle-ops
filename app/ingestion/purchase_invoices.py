import hashlib
import re
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal, InvalidOperation

from app.ingestion.amazon_reports.header_aliases import normalize_header
from app.ingestion.product_costs import load_rows


INVOICE_HEADER_ALIASES: dict[str, set[str]] = {
    "supplier_sku": {
        "Supplier SKU",
        "Supplier code",
        "Artikelnummer",
        "Artikelnr",
        "Kod dostawcy",
        "SKU dostawcy",
        "Код постачальника",
    },
    "sku": {
        "SKU",
        "Seller SKU",
        "MSKU",
        "Артикул",
    },
    "ean": {
        "EAN",
        "Barcode",
        "GTIN",
        "Kod EAN",
        "Штрихкод",
    },
    "product_name": {
        "Product",
        "Product name",
        "Description",
        "Item description",
        "Name",
        "Nazwa produktu",
        "Opis",
        "Produkt",
        "Artikel",
        "Bezeichnung",
        "Назва товару",
        "Опис",
    },
    "quantity": {
        "Quantity",
        "Qty",
        "QTY",
        "Ilość",
        "Ilosc",
        "Menge",
        "Anzahl",
        "Кількість",
    },
    "unit_cost": {
        "Unit cost",
        "Unit price",
        "Net unit price",
        "Purchase price",
        "Cena jednostkowa",
        "Cena netto",
        "Einzelpreis",
        "Stückpreis",
        "Stuckpreis",
        "Ціна",
        "Ціна за одиницю",
    },
    "line_net_amount": {
        "Line net",
        "Net amount",
        "Amount net",
        "Netto",
        "Wartość netto",
        "Wartosc netto",
        "Nettobetrag",
        "Сума без ПДВ",
    },
    "vat_rate_percent": {
        "VAT %",
        "VAT rate",
        "Tax rate",
        "MwSt %",
        "MwSt.",
        "VAT",
        "Stawka VAT",
        "ПДВ %",
    },
    "vat_amount": {
        "VAT amount",
        "Tax amount",
        "MwSt Betrag",
        "Kwota VAT",
        "ПДВ сума",
    },
    "line_gross_amount": {
        "Line total",
        "Gross amount",
        "Total",
        "Brutto",
        "Wartość brutto",
        "Wartosc brutto",
        "Gesamtbetrag",
        "Сума з ПДВ",
    },
}

REQUIRED_INVOICE_FIELDS = {"product_name", "quantity", "unit_cost"}
DATE_FORMATS = ("%Y-%m-%d", "%d.%m.%Y", "%d/%m/%Y", "%d-%m-%Y")
PRODUCT_LINE_TYPE = "product"
INBOUND_SHIPPING_LINE_TYPE = "inbound_shipping"
FULFILLMENT_FEE_LINE_TYPE = "fulfillment_fee"
MARKETPLACE_FEE_LINE_TYPE = "marketplace_fee"
SERVICE_LINE_TYPE = "service"
OTHER_LINE_TYPE = "other"
LINE_TYPE_CATEGORIES = {
    PRODUCT_LINE_TYPE: None,
    INBOUND_SHIPPING_LINE_TYPE: "inbound_shipping",
    FULFILLMENT_FEE_LINE_TYPE: "fulfillment",
    MARKETPLACE_FEE_LINE_TYPE: "marketplace_fee",
    SERVICE_LINE_TYPE: "service",
    OTHER_LINE_TYPE: "other",
}
LINE_TYPE_PATTERNS: list[tuple[str, str]] = [
    (
        INBOUND_SHIPPING_LINE_TYPE,
        r"(versand|versandkosten|shipping|delivery|freight|transport|transportkosten|porto|livraison|exp[eé]dition|spedizione|env[ií]o|transporte|wysy[lł]ka|dostawa|bezorg|verzend|frakt|leverans|доставка|транспорт|перевезення)",
    ),
    (
        FULFILLMENT_FEE_LINE_TYPE,
        r"(fulfillment|fulfilment|fba|prep|pick[ -]?pack|lager|warehouse|storage|handling|fulfillment[ -]?center|logistik|logistics|magazyn|magazynowanie|склад|фулфілмент)",
    ),
    (
        MARKETPLACE_FEE_LINE_TYPE,
        r"(amazon fee|marketplace fee|referral fee|commission|provision|verkaufsgeb[uü]hr|geb[uü]hr|commissione|comisi[oó]n|prowizja|комісія)",
    ),
    (
        SERVICE_LINE_TYPE,
        r"(service|dienstleistung|servicio|servizi|us[lł]uga|servicekosten|сервіс|послуга)",
    ),
]
PDF_HEADERS = [
    "Supplier SKU",
    "SKU",
    "EAN",
    "Product name",
    "Quantity",
    "VAT %",
    "Unit cost",
    "Line net",
]


@dataclass(frozen=True)
class PurchaseInvoicePreview:
    filename: str
    supplier_name: str
    invoice_number: str | None
    invoice_date: date | None
    due_date: date | None
    currency: str
    headers: list[str]
    mapping: dict[str, str]
    missing_fields: list[str]
    ambiguous_headers: dict[str, list[str]]
    unknown_headers: list[str]
    row_count: int
    raw_rows: list[dict[str, str]]
    parsed_rows: list[dict[str, str | Decimal | None]]
    sample_rows: list[dict[str, str]]
    normalized_sample_rows: list[dict[str, str | float | None]]
    totals: dict[str, float]
    validation_errors: list[str]

    @property
    def can_commit(self) -> bool:
        return not self.missing_fields and not self.ambiguous_headers and not self.validation_errors


def calculate_sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def is_pdf(filename: str, content: bytes) -> bool:
    return filename.lower().endswith(".pdf") or content.startswith(b"%PDF")


def extract_pdf_text(content: bytes) -> str:
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise ValueError("PDF import requires the pypdf package.") from exc

    from io import BytesIO

    try:
        reader = PdfReader(BytesIO(content), strict=False)
    except Exception as exc:
        raise ValueError(f"Could not read PDF: {exc}") from exc

    page_texts: list[str] = []
    page_errors: list[str] = []
    for index, page in enumerate(reader.pages, start=1):
        try:
            text = page.extract_text() or ""
        except Exception as exc:
            page_errors.append(f"page {index}: {exc}")
            continue
        if text.strip():
            page_texts.append(text)

    if not page_texts:
        details = f" ({'; '.join(page_errors)})" if page_errors else ""
        raise ValueError(f"PDF has no extractable text{details}. OCR/repair is needed.")

    return "\n".join(page_texts)


def first_regex(text: str, patterns: list[str]) -> str | None:
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE)
        if match:
            return match.group(1).strip()
    return None


def extract_pdf_metadata(text: str) -> dict[str, str | date | None]:
    invoice_number = first_regex(
        text,
        [
            r"(?:Rechnungs-Nr\.?|Rechnungsnummer|Invoice\s*(?:No\.?|Number)|Facture\s*(?:N[°o]\.?|numéro)|Fattura\s*(?:n\.?|numero)|Factura\s*(?:n[ºo]\.?|número)|Faktura\s*(?:nr|numer)|Factuurnummer|Fakturanummer)\s*[:#]?\s*([A-Z0-9][A-Z0-9\-/]+)",
        ],
    )
    invoice_date_value = first_regex(
        text,
        [
            r"^\s*(?:Datum|Rechnungsdatum|Invoice\s*date|Date\s*de\s*facture|Data\s*fattura|Fecha\s*factura|Data\s*wystawienia|Factuurdatum|Fakturadatum)\s*[:#]?\s*(\d{1,2}[./-]\d{1,2}[./-]\d{2,4})\s*$",
        ],
    )
    due_date_value = first_regex(
        text,
        [
            r"(?:Fälligkeitsdatum|Zahlbar\s*bis|Due\s*date|Date\s*d['’]échéance|Scadenza|Vencimiento|Termin\s*płatności|Vervaldatum)\s*[:#]?\s*(\d{1,2}[./-]\d{1,2}[./-]\d{2,4})",
        ],
    )

    supplier_name = None
    for line in text.splitlines():
        clean = line.strip()
        if re.search(r"\b(GmbH|AG|S\.?A\.?|S\.?L\.?|S\.?r\.?l\.?|Sp\.?\s*z\.?\s*o\.?\s*o\.?|B\.?V\.?|AB|SARL|SAS|Ltd\.?|Limited)\b", clean):
            supplier_name = clean.split("|")[0].strip()
            break

    return {
        "supplier_name": supplier_name,
        "invoice_number": invoice_number,
        "invoice_date": parse_date(invoice_date_value) if invoice_date_value else None,
        "due_date": parse_date(due_date_value) if due_date_value else None,
    }


def looks_like_supplier_sku(value: str) -> bool:
    return bool(re.match(r"^[A-Z]{0,4}\d[A-Z0-9\-_./]*$", value, flags=re.IGNORECASE))


def parse_pdf_invoice_rows(text: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    active: dict[str, str] | None = None
    product_parts: list[str] = []

    amount_pattern = re.compile(
        r"^\s*(?P<quantity>\d+(?:[.,]\d+)?)\s+"
        r"(?P<vat>\d+(?:[.,]\d+)?)\s*%\s+"
        r"(?P<unit>[-0-9.,\s]+)(?:€|EUR|zł|PLN|kr|SEK|£|GBP)?\s+"
        r"(?P<net>[-0-9.,\s]+)(?:€|EUR|zł|PLN|kr|SEK|£|GBP)?\s*$",
        flags=re.IGNORECASE,
    )
    single_line_pattern = re.compile(
        r"^\s*(?P<position>\d{1,4})\s+"
        r"(?P<product>.+?)\s+"
        r"(?P<quantity>\d+(?:[.,]\d+)?)\s+"
        r"(?P<vat>\d+(?:[.,]\d+)?)\s*%\s+"
        r"(?P<unit>[-0-9.,\s]+)(?:€|EUR|zł|PLN|kr|SEK|£|GBP)?\s+"
        r"(?P<net>[-0-9.,\s]+)(?:€|EUR|zł|PLN|kr|SEK|£|GBP)?\s*$",
        flags=re.IGNORECASE,
    )
    start_pattern = re.compile(r"^\s*(?P<position>\d{1,4})\s+(?P<rest>.+)$")

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        single_line_match = single_line_pattern.match(line)
        if single_line_match and active is None:
            product_value = single_line_match.group("product").strip()
            token, _, product_name = product_value.partition(" ")
            supplier_sku = token if product_name and looks_like_supplier_sku(token) else ""
            if not supplier_sku:
                product_name = product_value
            rows.append(
                {
                    "Supplier SKU": supplier_sku,
                    "SKU": supplier_sku,
                    "EAN": "",
                    "Product name": product_name.strip(),
                    "Quantity": single_line_match.group("quantity"),
                    "VAT %": single_line_match.group("vat"),
                    "Unit cost": single_line_match.group("unit"),
                    "Line net": single_line_match.group("net"),
                }
            )
            continue

        amount_match = amount_pattern.match(line)
        if amount_match and active is not None:
            active["Product name"] = " ".join(product_parts).strip()
            active["Quantity"] = amount_match.group("quantity")
            active["VAT %"] = amount_match.group("vat")
            active["Unit cost"] = amount_match.group("unit")
            active["Line net"] = amount_match.group("net")
            rows.append(active)
            active = None
            product_parts = []
            continue

        if active is not None:
            ean_match = re.search(r"\b(?:EAN|GTIN|Barcode|Code[- ]barres|Codice\s*EAN|Código\s*EAN|Kod\s*EAN)\s*[:#]?\s*([0-9]{8,14})\b", line, flags=re.IGNORECASE)
            if ean_match:
                active["EAN"] = ean_match.group(1)
                continue
            if re.search(r"(Zolltarif|Herkunftsland|customs|origin|taric|hs\s*code)", line, flags=re.IGNORECASE):
                continue
            product_parts.append(line)
            continue

        start_match = start_pattern.match(line)
        if not start_match:
            continue

        rest = start_match.group("rest").strip()
        if rest.lower().startswith(("pos.", "prod.", "produkt", "product", "gesamt", "anzahl")):
            continue

        token, _, product_name = rest.partition(" ")
        supplier_sku = token if product_name and looks_like_supplier_sku(token) else ""
        if not supplier_sku:
            product_name = rest
        active = {
            "Supplier SKU": supplier_sku,
            "SKU": supplier_sku,
            "EAN": "",
            "Product name": product_name.strip(),
            "Quantity": "",
            "VAT %": "",
            "Unit cost": "",
            "Line net": "",
        }
        product_parts = [product_name.strip()]

    return rows


def load_invoice_rows(filename: str, content: bytes) -> tuple[list[str], list[dict[str, str]], dict[str, str | date | None]]:
    if not is_pdf(filename, content):
        headers, rows = load_rows(filename, content)
        return headers, rows, {}

    text = extract_pdf_text(content)
    metadata = extract_pdf_metadata(text)
    rows = parse_pdf_invoice_rows(text)
    return PDF_HEADERS, rows, metadata


def detect_invoice_mapping(headers: list[str]) -> tuple[dict[str, str], list[str], dict[str, list[str]], list[str]]:
    normalized_aliases = {
        canonical: {normalize_header(alias) for alias in aliases}
        for canonical, aliases in INVOICE_HEADER_ALIASES.items()
    }
    mapping: dict[str, str] = {}
    ambiguous_headers: dict[str, list[str]] = {}
    matched_headers: set[str] = set()

    for header in headers:
        normalized = normalize_header(header)
        matches = [
            canonical
            for canonical, aliases in normalized_aliases.items()
            if normalized in aliases
        ]
        if len(matches) == 1:
            canonical = matches[0]
            if canonical in mapping:
                ambiguous_headers.setdefault(header, []).append(canonical)
            else:
                mapping[canonical] = header
                matched_headers.add(header)
        elif len(matches) > 1:
            ambiguous_headers[header] = matches

    missing_fields = sorted(REQUIRED_INVOICE_FIELDS - set(mapping))
    unknown_headers = [header for header in headers if header not in matched_headers]
    return mapping, missing_fields, ambiguous_headers, unknown_headers


def parse_decimal(value: str | int | float | None, default: Decimal | None = None) -> Decimal | None:
    if value is None or value == "":
        return default
    normalized = str(value).strip().replace("\u00a0", "").replace(" ", "")
    normalized = re.sub(r"[^0-9,.\-]", "", normalized)
    if "," in normalized and "." in normalized:
        normalized = normalized.replace(".", "").replace(",", ".")
    elif "," in normalized:
        normalized = normalized.replace(",", ".")
    try:
        return Decimal(normalized)
    except InvalidOperation as exc:
        raise ValueError(f"Invalid number: {value}") from exc


def parse_date(value: str | date | None) -> date | None:
    if value is None or value == "":
        return None
    if isinstance(value, date):
        return value
    clean = str(value).strip()
    for date_format in DATE_FORMATS:
        try:
            return datetime.strptime(clean, date_format).date()
        except ValueError:
            continue
    raise ValueError(f"Unsupported date: {value}")


def decimal_to_float(value: Decimal | None) -> float | None:
    if value is None:
        return None
    return float(value.quantize(Decimal("0.01")))


def serialize_row(row: dict[str, str | Decimal | None]) -> dict[str, str | float | None]:
    serialized: dict[str, str | float | None] = {}
    for key, value in row.items():
        serialized[key] = decimal_to_float(value) if isinstance(value, Decimal) else value
    return serialized


def classify_invoice_line(
    product_name: str,
    sku: str | None = None,
    supplier_sku: str | None = None,
    ean: str | None = None,
) -> tuple[str, str | None]:
    normalized_name = normalize_header(product_name)
    for line_type, pattern in LINE_TYPE_PATTERNS:
        if re.search(pattern, normalized_name, flags=re.IGNORECASE):
            return line_type, LINE_TYPE_CATEGORIES[line_type]
    if sku or supplier_sku or ean:
        return PRODUCT_LINE_TYPE, None
    return OTHER_LINE_TYPE, LINE_TYPE_CATEGORIES[OTHER_LINE_TYPE]


def build_purchase_invoice_preview(
    filename: str,
    content: bytes,
    supplier_name: str,
    invoice_number: str | None = None,
    invoice_date: date | None = None,
    due_date: date | None = None,
    currency: str = "EUR",
    sample_size: int = 10,
) -> PurchaseInvoicePreview:
    headers, rows, metadata = load_invoice_rows(filename, content)
    supplier = supplier_name.strip() or str(metadata.get("supplier_name") or "")
    resolved_invoice_number = invoice_number.strip() if invoice_number else metadata.get("invoice_number")
    resolved_invoice_date = invoice_date or metadata.get("invoice_date")
    resolved_due_date = due_date or metadata.get("due_date")
    mapping, missing_fields, ambiguous_headers, unknown_headers = detect_invoice_mapping(headers)
    validation_errors: list[str] = []
    parsed_rows: list[dict[str, str | Decimal | None]] = []

    if not headers:
        validation_errors.append("File has no header row.")
    if not rows:
        validation_errors.append("File has no data rows.")
    if not supplier:
        validation_errors.append("Supplier name is required.")

    if not missing_fields and not ambiguous_headers:
        for row_number, row in enumerate(rows, start=2):
            try:
                quantity = parse_decimal(row.get(mapping["quantity"]), Decimal("0"))
                unit_cost = parse_decimal(row.get(mapping["unit_cost"]), Decimal("0"))
                if quantity is None or quantity <= 0:
                    validation_errors.append(f"Row {row_number}: Quantity must be greater than zero")
                    continue
                if unit_cost is None or unit_cost < 0:
                    validation_errors.append(f"Row {row_number}: Unit cost must be zero or greater")
                    continue
                product_name = str(row.get(mapping["product_name"], "")).strip()
                if not product_name:
                    validation_errors.append(f"Row {row_number}: Product name is required")
                    continue

                line_net = parse_decimal(row.get(mapping.get("line_net_amount")), None)
                if line_net is None:
                    line_net = (quantity * unit_cost).quantize(Decimal("0.01"))
                vat_rate = parse_decimal(row.get(mapping.get("vat_rate_percent")), None)
                vat_amount = parse_decimal(row.get(mapping.get("vat_amount")), None)
                gross = parse_decimal(row.get(mapping.get("line_gross_amount")), None)
                if vat_amount is None and vat_rate is not None and line_net is not None:
                    vat_amount = (line_net * vat_rate / Decimal("100")).quantize(Decimal("0.01"))
                if gross is None and line_net is not None and vat_amount is not None:
                    gross = (line_net + vat_amount).quantize(Decimal("0.01"))
                supplier_sku = str(row.get(mapping.get("supplier_sku", ""), "")).strip() or None
                sku = str(row.get(mapping.get("sku", ""), "")).strip() or None
                ean = str(row.get(mapping.get("ean", ""), "")).strip() or None
                line_type, expense_category = classify_invoice_line(
                    product_name=product_name,
                    sku=sku,
                    supplier_sku=supplier_sku,
                    ean=ean,
                )

                parsed_rows.append(
                    {
                        "supplier_sku": supplier_sku,
                        "sku": sku,
                        "ean": ean,
                        "line_type": line_type,
                        "expense_category": expense_category,
                        "product_name": product_name,
                        "quantity": quantity,
                        "unit_cost": unit_cost,
                        "line_net_amount": line_net,
                        "vat_rate_percent": vat_rate,
                        "vat_amount": vat_amount,
                        "line_gross_amount": gross,
                        "currency": currency.upper(),
                    }
                )
            except ValueError as exc:
                validation_errors.append(f"Row {row_number}: {exc}")

    subtotal = sum((row["line_net_amount"] for row in parsed_rows if isinstance(row["line_net_amount"], Decimal)), Decimal("0"))
    vat_total = sum((row["vat_amount"] for row in parsed_rows if isinstance(row["vat_amount"], Decimal)), Decimal("0"))
    gross_total = sum((row["line_gross_amount"] for row in parsed_rows if isinstance(row["line_gross_amount"], Decimal)), Decimal("0"))
    product_subtotal = sum((row["line_net_amount"] for row in parsed_rows if row.get("line_type") == PRODUCT_LINE_TYPE and isinstance(row["line_net_amount"], Decimal)), Decimal("0"))
    expense_subtotal = sum((row["line_net_amount"] for row in parsed_rows if row.get("line_type") != PRODUCT_LINE_TYPE and isinstance(row["line_net_amount"], Decimal)), Decimal("0"))
    product_quantity = sum((row["quantity"] for row in parsed_rows if row.get("line_type") == PRODUCT_LINE_TYPE and isinstance(row["quantity"], Decimal)), Decimal("0"))
    total_line_quantity = sum((row["quantity"] for row in parsed_rows if isinstance(row["quantity"], Decimal)), Decimal("0"))

    return PurchaseInvoicePreview(
        filename=filename,
        supplier_name=supplier,
        invoice_number=str(resolved_invoice_number) if resolved_invoice_number else None,
        invoice_date=resolved_invoice_date if isinstance(resolved_invoice_date, date) else None,
        due_date=resolved_due_date if isinstance(resolved_due_date, date) else None,
        currency=currency.upper(),
        headers=headers,
        mapping=mapping,
        missing_fields=missing_fields,
        ambiguous_headers=ambiguous_headers,
        unknown_headers=unknown_headers,
        row_count=len(rows),
        raw_rows=rows,
        parsed_rows=parsed_rows,
        sample_rows=rows[:sample_size],
        normalized_sample_rows=[serialize_row(row) for row in parsed_rows[:sample_size]],
        totals={
            "subtotal_amount": decimal_to_float(subtotal) or 0,
            "vat_amount": decimal_to_float(vat_total) or 0,
            "total_amount": decimal_to_float(gross_total if gross_total else subtotal + vat_total) or 0,
            "quantity": float(product_quantity),
            "line_quantity": float(total_line_quantity),
            "product_subtotal_amount": decimal_to_float(product_subtotal) or 0,
            "expense_subtotal_amount": decimal_to_float(expense_subtotal) or 0,
        },
        validation_errors=validation_errors,
    )
