import csv
import hashlib
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from io import BytesIO, StringIO

import pandas as pd

from app.ingestion.amazon_reports.header_aliases import normalize_header
from app.ingestion.amazon_reports.payment_transactions import decode_csv, detect_delimiter


PRODUCT_COST_HEADER_ALIASES: dict[str, set[str]] = {
    "product_name": {
        "Nazwa produktu",
        "Product name",
        "Produktname",
        "Nom du produit",
        "Nome prodotto",
        "Nombre del producto",
        "Productnaam",
        "Produktnamn",
    },
    "sku": {
        "SKU",
        "Seller SKU",
        "MSKU",
    },
    "purchase_cost": {
        "Zakup €",
        "Zakup EUR",
        "Zakup",
        "Purchase cost",
        "Purchase cost EUR",
        "Cost",
        "Cost EUR",
    },
}

REQUIRED_PRODUCT_COST_FIELDS = {"sku", "purchase_cost"}


@dataclass(frozen=True)
class ProductCostPreview:
    filename: str
    currency: str
    effective_date: date
    headers: list[str]
    mapping: dict[str, str]
    missing_fields: list[str]
    ambiguous_headers: dict[str, list[str]]
    unknown_headers: list[str]
    row_count: int
    raw_rows: list[dict[str, str]]
    parsed_rows: list[dict[str, str | Decimal | date | None]]
    sample_rows: list[dict[str, str]]
    normalized_sample_rows: list[dict[str, str | float | None]]
    validation_errors: list[str]

    @property
    def can_commit(self) -> bool:
        return not self.missing_fields and not self.ambiguous_headers and not self.validation_errors


def calculate_sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def detect_product_cost_mapping(headers: list[str]) -> tuple[dict[str, str], list[str], dict[str, list[str]], list[str]]:
    normalized_aliases = {
        canonical: {normalize_header(alias) for alias in aliases}
        for canonical, aliases in PRODUCT_COST_HEADER_ALIASES.items()
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

    missing_fields = sorted(REQUIRED_PRODUCT_COST_FIELDS - set(mapping))
    unknown_headers = [header for header in headers if header not in matched_headers]
    return mapping, missing_fields, ambiguous_headers, unknown_headers


def parse_decimal(value: str | int | float | None) -> Decimal:
    if value is None or value == "":
        raise ValueError("Missing purchase cost")
    normalized = str(value).strip().replace("\u00a0", "").replace(" ", "")
    if "," in normalized and "." in normalized:
        normalized = normalized.replace(".", "").replace(",", ".")
    elif "," in normalized:
        normalized = normalized.replace(",", ".")
    try:
        return Decimal(normalized)
    except InvalidOperation as exc:
        raise ValueError(f"Invalid purchase cost: {value}") from exc


def detect_currency(headers: list[str]) -> str:
    return "EUR"


def load_rows(filename: str, content: bytes) -> tuple[list[str], list[dict[str, str]]]:
    lower = filename.lower()
    if lower.endswith(".xlsx") or lower.endswith(".xls"):
        dataframe = pd.read_excel(BytesIO(content)).fillna("")
        rows = [
            {str(key): str(value) for key, value in record.items()}
            for record in dataframe.to_dict(orient="records")
        ]
        return [str(column) for column in dataframe.columns], rows

    text, _ = decode_csv(content)
    delimiter = detect_delimiter(text)
    reader = csv.DictReader(StringIO(text), delimiter=delimiter)
    return list(reader.fieldnames or []), list(reader)


def serialize_row(row: dict[str, str | Decimal | date | None]) -> dict[str, str | float | None]:
    serialized: dict[str, str | float | None] = {}
    for key, value in row.items():
        if isinstance(value, Decimal):
            serialized[key] = float(value.quantize(Decimal("0.01")))
        elif isinstance(value, date):
            serialized[key] = value.isoformat()
        else:
            serialized[key] = value
    return serialized


def build_product_cost_preview(
    filename: str,
    content: bytes,
    effective_date: date | None = None,
    sample_size: int = 10,
) -> ProductCostPreview:
    headers, rows = load_rows(filename, content)
    mapping, missing_fields, ambiguous_headers, unknown_headers = detect_product_cost_mapping(headers)
    detected_currency = detect_currency(headers)
    effective = effective_date or datetime.utcnow().date()

    validation_errors: list[str] = []
    parsed_rows: list[dict[str, str | Decimal | date | None]] = []

    if not headers:
        validation_errors.append("File has no header row.")
    if not rows:
        validation_errors.append("File has no data rows.")

    if not missing_fields and not ambiguous_headers:
        for row_number, row in enumerate(rows, start=2):
            sku = str(row.get(mapping["sku"], "")).strip()
            if not sku:
                validation_errors.append(f"Row {row_number}: Missing SKU")
                continue
            try:
                purchase_cost = parse_decimal(row.get(mapping["purchase_cost"]))
            except ValueError as exc:
                validation_errors.append(f"Row {row_number}: {exc}")
                continue

            parsed_rows.append(
                {
                    "sku": sku,
                    "product_name": str(row.get(mapping.get("product_name", ""), "")).strip() or None,
                    "purchase_cost": purchase_cost,
                    "currency": detected_currency,
                    "effective_date": effective,
                }
            )

    return ProductCostPreview(
        filename=filename,
        currency=detected_currency,
        effective_date=effective,
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
        validation_errors=validation_errors,
    )
