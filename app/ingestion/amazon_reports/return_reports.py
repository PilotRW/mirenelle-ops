import csv
import hashlib
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation
from io import StringIO


REPORT_TYPE_CUSTOMER_RETURNS = "GET_FBA_FULFILLMENT_CUSTOMER_RETURNS_DATA"

RETURN_FIELDS = {
    "return_date": "return-date",
    "order_id": "order-id",
    "sku": "sku",
    "asin": "asin",
    "fnsku": "fnsku",
    "product_name": "product-name",
    "quantity": "quantity",
    "fulfillment_center_id": "fulfillment-center-id",
    "detailed_disposition": "detailed-disposition",
    "reason": "reason",
    "status": "status",
    "license_plate_number": "license-plate-number",
    "customer_comments": "customer-comments",
}
REQUIRED_RETURN_FIELDS = {"return_date", "order_id", "sku", "fnsku", "quantity"}


@dataclass(frozen=True)
class ReturnReportPreview:
    filename: str
    encoding: str
    delimiter: str
    headers: list[str]
    mapping: dict[str, str]
    missing_fields: list[str]
    unknown_headers: list[str]
    row_count: int
    parsed_rows: list[dict]
    sample_rows: list[dict[str, str]]
    validation_errors: list[str]

    @property
    def can_commit(self) -> bool:
        return not self.missing_fields and not self.validation_errors


def calculate_sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def _decode(content: bytes) -> tuple[str, str]:
    for encoding in ("utf-8-sig", "utf-8", "cp1252"):
        try:
            return content.decode(encoding), encoding
        except UnicodeDecodeError:
            continue
    return content.decode("utf-8", errors="replace"), "utf-8-replace"


def _parse_datetime(value: str) -> datetime:
    return datetime.fromisoformat(value.strip().replace("Z", "+00:00")).replace(tzinfo=None)


def _parse_decimal(value: str) -> Decimal:
    try:
        return Decimal((value or "0").strip().replace(",", "."))
    except InvalidOperation:
        return Decimal("0")


def build_return_report_preview(
    filename: str,
    content: bytes,
    marketplace: str,
    sample_size: int = 10,
) -> ReturnReportPreview:
    text, encoding = _decode(content)
    reader = csv.DictReader(StringIO(text), delimiter="\t")
    headers = [header.strip() for header in (reader.fieldnames or [])]
    mapping = {
        canonical: header
        for canonical, header in RETURN_FIELDS.items()
        if header in headers
    }
    missing_fields = sorted(REQUIRED_RETURN_FIELDS - mapping.keys())
    unknown_headers = sorted(set(headers) - set(mapping.values()))
    parsed_rows: list[dict] = []
    sample_rows: list[dict[str, str]] = []
    validation_errors: list[str] = []

    for index, row in enumerate(reader, start=2):
        clean = {(key or "").strip(): (value or "").strip() for key, value in row.items()}
        if index <= sample_size + 1:
            sample_rows.append(clean)
        if missing_fields:
            continue
        try:
            parsed_rows.append(
                {
                    "marketplace": marketplace,
                    "return_date": _parse_datetime(clean[mapping["return_date"]]),
                    "order_id": clean[mapping["order_id"]],
                    "sku": clean[mapping["sku"]],
                    "asin": clean.get(mapping.get("asin", "")) or None,
                    "fnsku": clean[mapping["fnsku"]],
                    "product_name": clean.get(mapping.get("product_name", "")) or None,
                    "quantity": _parse_decimal(clean[mapping["quantity"]]),
                    "fulfillment_center_id": clean.get(mapping.get("fulfillment_center_id", "")) or None,
                    "detailed_disposition": clean.get(mapping.get("detailed_disposition", "")) or None,
                    "reason": clean.get(mapping.get("reason", "")) or None,
                    "status": clean.get(mapping.get("status", "")) or None,
                    "license_plate_number": clean.get(mapping.get("license_plate_number", "")) or "",
                    "customer_comments": clean.get(mapping.get("customer_comments", "")) or None,
                    "raw_row": clean,
                }
            )
        except (KeyError, ValueError) as exc:
            validation_errors.append(f"Row {index}: {exc}")

    return ReturnReportPreview(
        filename=filename,
        encoding=encoding,
        delimiter="\t",
        headers=headers,
        mapping=mapping,
        missing_fields=missing_fields,
        unknown_headers=unknown_headers,
        row_count=len(parsed_rows),
        parsed_rows=parsed_rows,
        sample_rows=sample_rows,
        validation_errors=validation_errors,
    )
