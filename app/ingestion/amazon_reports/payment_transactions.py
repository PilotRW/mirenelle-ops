import csv
import hashlib
import re
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from io import StringIO

from app.ingestion.amazon_reports.header_aliases import (
    HeaderMappingResult,
    detect_payment_transaction_mapping,
)


DATE_FORMATS = (
    "%d/%m/%Y",
    "%d.%m.%Y",
    "%Y-%m-%d",
    "%d.%m.%Y %H:%M:%S UTC",
    "%d/%m/%Y %H:%M:%S UTC",
    "%Y-%m-%d %H:%M:%S UTC",
)


@dataclass(frozen=True)
class PaymentTransactionPreview:
    filename: str
    encoding: str
    delimiter: str
    headers: list[str]
    mapping_result: HeaderMappingResult
    row_count: int
    currency: str | None
    raw_rows: list[dict[str, str]]
    sample_rows: list[dict[str, str]]
    normalized_sample_rows: list[dict[str, str | int | float | None]]
    totals_by_transaction_type: dict[str, dict[str, int | float]]
    validation_errors: list[str]
    parsed_rows: list[dict[str, str | date | Decimal | None]]

    @property
    def can_commit(self) -> bool:
        return (
            not self.mapping_result.missing_fields
            and not self.mapping_result.ambiguous_headers
            and not self.validation_errors
        )


def decode_csv(content: bytes) -> tuple[str, str]:
    for encoding in ("utf-8-sig", "utf-8", "cp1252"):
        try:
            return content.decode(encoding), encoding
        except UnicodeDecodeError:
            continue
    return content.decode("utf-8", errors="replace"), "utf-8-replace"


def detect_delimiter(text: str) -> str:
    sample = text[:4096]
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=",;\t")
        return dialect.delimiter
    except csv.Error:
        return ","


def find_header_start(text: str, delimiter: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        try:
            cells = next(csv.reader([line], delimiter=delimiter))
        except csv.Error:
            continue
        mapping = detect_payment_transaction_mapping(cells)
        mapped_required_fields = REQUIRED_PREVIEW_HEADER_FIELDS - set(mapping.missing_fields)
        if len(mapped_required_fields) >= 5:
            return "\n".join(lines[index:])
    return text


REQUIRED_PREVIEW_HEADER_FIELDS = {
    "transaction_date",
    "transaction_type",
    "external_transaction_id",
    "product_details",
    "product_charges",
    "total_amount",
}


def extract_currency(headers: list[str], total_header: str | None, text: str = "") -> str | None:
    candidates = [total_header] if total_header else []
    candidates.extend(headers)
    for header in candidates:
        if not header:
            continue
        match = re.search(r"\(([A-Z]{3})\)", header)
        if match:
            return match.group(1)
    normalized_text = text.casefold()
    if any(marker in normalized_text for marker in ("euro", "eur", "euros")):
        return "EUR"
    if any(marker in normalized_text for marker in ("svenska kronor", "kronor", "sek")):
        return "SEK"
    if any(marker in normalized_text for marker in ("zł", "zloty", "złoty", "pln")):
        return "PLN"
    if any(marker in normalized_text for marker in ("pound", "gbp", "sterling")):
        return "GBP"
    return None


def parse_decimal(value: str | None) -> Decimal:
    if value is None or value == "":
        return Decimal("0")
    normalized = value.strip().replace("\u00a0", "").replace(" ", "")
    if "," in normalized and "." in normalized:
        normalized = normalized.replace(".", "").replace(",", ".")
    elif "," in normalized:
        normalized = normalized.replace(",", ".")
    try:
        return Decimal(normalized)
    except InvalidOperation as exc:
        raise ValueError(f"Invalid decimal value: {value}") from exc


def parse_date(value: str | None) -> date:
    if not value:
        raise ValueError("Missing date value")
    clean = value.strip()
    for date_format in DATE_FORMATS:
        try:
            return datetime.strptime(clean, date_format).date()
        except ValueError:
            continue
    raise ValueError(f"Unsupported date value: {value}")


def decimal_to_float(value: Decimal | float | int | None) -> float:
    if value is None:
        return 0.0
    if not isinstance(value, Decimal):
        value = Decimal(str(value))
    return float(value.quantize(Decimal("0.01")))


def parse_payment_transaction_row(
    row: dict[str, str],
    mapping: dict[str, str],
    currency: str | None,
) -> dict[str, str | date | Decimal | None]:
    amazon_fees = parse_decimal(row.get(mapping["amazon_fees"]))
    if "fba_fees" in mapping:
        amazon_fees += parse_decimal(row.get(mapping["fba_fees"]))
    if "other_transaction_fees" in mapping:
        amazon_fees += parse_decimal(row.get(mapping["other_transaction_fees"]))
    return {
        "transaction_date": parse_date(row.get(mapping["transaction_date"])),
        "transaction_status": row.get(mapping["transaction_status"]),
        "transaction_type": row.get(mapping["transaction_type"]),
        "external_transaction_id": row.get(mapping["external_transaction_id"]),
        "sku": row.get(mapping["sku"]) if "sku" in mapping else None,
        "quantity": parse_decimal(row.get(mapping["quantity"])) if "quantity" in mapping else None,
        "product_details": row.get(mapping["product_details"]),
        "product_charges": parse_decimal(row.get(mapping["product_charges"])),
        "promotional_rebates": parse_decimal(row.get(mapping["promotional_rebates"])),
        "amazon_fees": amazon_fees,
        "other_amount": parse_decimal(row.get(mapping["other_amount"])),
        "total_amount": parse_decimal(row.get(mapping["total_amount"])),
        "currency": currency,
    }


def serialize_payment_transaction_row(
    row: dict[str, str | date | Decimal | None],
) -> dict[str, str | int | float | None]:
    serialized: dict[str, str | int | float | None] = {}
    for key, value in row.items():
        if isinstance(value, date):
            serialized[key] = value.isoformat()
        elif isinstance(value, Decimal):
            serialized[key] = decimal_to_float(value)
        else:
            serialized[key] = value
    return serialized


def calculate_sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def build_payment_transaction_preview(
    filename: str,
    content: bytes,
    sample_size: int = 10,
) -> PaymentTransactionPreview:
    text, encoding = decode_csv(content)
    delimiter = detect_delimiter(text)
    csv_text = find_header_start(text, delimiter)

    reader = csv.DictReader(StringIO(csv_text), delimiter=delimiter)
    headers = list(reader.fieldnames or [])
    rows = [
        {str(key): str(value or "") for key, value in row.items() if key is not None}
        for row in reader
    ]

    mapping_result = detect_payment_transaction_mapping(headers)
    total_header = mapping_result.mapping.get("total_amount")
    currency = extract_currency(headers, total_header, text)

    validation_errors: list[str] = []
    normalized_sample_rows: list[dict[str, str | int | float | None]] = []
    parsed_rows: list[dict[str, str | date | Decimal | None]] = []
    totals_by_transaction_type: dict[str, dict[str, int | float]] = {}

    if not headers:
        validation_errors.append("CSV file has no header row.")

    if not rows:
        validation_errors.append("CSV file has no data rows.")

    if not currency:
        validation_errors.append("Could not detect currency from amount headers.")

    if not mapping_result.missing_fields and not mapping_result.ambiguous_headers:
        for row_number, row in enumerate(rows, start=2):
            try:
                parsed = parse_payment_transaction_row(row, mapping_result.mapping, currency)
            except ValueError as exc:
                validation_errors.append(f"Row {row_number}: {exc}")
                if len(validation_errors) >= 20:
                    validation_errors.append("Validation stopped after 20 errors.")
                    break
                continue

            parsed_rows.append(parsed)
            transaction_type = str(parsed["transaction_type"] or "")
            type_totals = totals_by_transaction_type.setdefault(
                transaction_type,
                {
                    "rows": 0,
                    "product_charges": 0.0,
                    "promotional_rebates": 0.0,
                    "amazon_fees": 0.0,
                    "other_amount": 0.0,
                    "total_amount": 0.0,
                },
            )
            type_totals["rows"] = int(type_totals["rows"]) + 1
            for field in (
                "product_charges",
                "promotional_rebates",
                "amazon_fees",
                "other_amount",
                "total_amount",
            ):
                type_totals[field] = round(float(type_totals[field]) + float(parsed[field] or 0), 2)

            if len(normalized_sample_rows) < sample_size:
                normalized_sample_rows.append(serialize_payment_transaction_row(parsed))

    return PaymentTransactionPreview(
        filename=filename,
        encoding=encoding,
        delimiter=delimiter,
        headers=headers,
        mapping_result=mapping_result,
        row_count=len(rows),
        currency=currency,
        raw_rows=rows,
        sample_rows=rows[:sample_size],
        normalized_sample_rows=normalized_sample_rows,
        totals_by_transaction_type=totals_by_transaction_type,
        validation_errors=validation_errors,
        parsed_rows=parsed_rows,
    )
