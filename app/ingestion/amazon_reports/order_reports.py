import csv
import hashlib
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation
from io import StringIO


REPORT_TYPE_ALL_ORDERS_BY_ORDER_DATE = "GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_GENERAL"

ORDER_HEADER_ALIASES: dict[str, set[str]] = {
    "amazon_order_id": {"amazon-order-id", "order-id"},
    "merchant_order_id": {"merchant-order-id"},
    "purchase_date": {"purchase-date"},
    "last_updated_date": {"last-updated-date"},
    "order_status": {"order-status"},
    "fulfillment_channel": {"fulfillment-channel"},
    "sales_channel": {"sales-channel"},
    "ship_service_level": {"ship-service-level"},
    "product_name": {"product-name"},
    "sku": {"sku"},
    "asin": {"asin"},
    "item_status": {"item-status"},
    "quantity": {"quantity", "quantity-purchased"},
    "currency": {"currency"},
    "item_price": {"item-price"},
    "item_tax": {"item-tax"},
    "shipping_price": {"shipping-price"},
    "shipping_tax": {"shipping-tax"},
    "item_promotion_discount": {"item-promotion-discount"},
    "ship_promotion_discount": {"ship-promotion-discount"},
}

REQUIRED_ORDER_FIELDS = {
    "amazon_order_id",
    "purchase_date",
    "fulfillment_channel",
    "sku",
    "quantity",
}


@dataclass(frozen=True)
class OrderReportPreview:
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
    totals: dict[str, float | int]
    validation_errors: list[str]

    @property
    def can_commit(self) -> bool:
        return not self.missing_fields and not self.validation_errors


def calculate_sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def decode_report(content: bytes) -> tuple[str, str]:
    for encoding in ("utf-8-sig", "utf-8", "cp1252"):
        try:
            return content.decode(encoding), encoding
        except UnicodeDecodeError:
            continue
    return content.decode("utf-8", errors="replace"), "utf-8-replace"


def detect_delimiter(text: str) -> str:
    sample = text[:4096]
    try:
        return csv.Sniffer().sniff(sample, delimiters="\t,;").delimiter
    except csv.Error:
        return "\t"


def normalize_header(value: str) -> str:
    return value.strip().replace("\ufeff", "").casefold()


def detect_mapping(headers: list[str]) -> tuple[dict[str, str], list[str], list[str]]:
    normalized_headers = {normalize_header(header): header for header in headers}
    mapping: dict[str, str] = {}
    for canonical, aliases in ORDER_HEADER_ALIASES.items():
        for alias in aliases:
            header = normalized_headers.get(normalize_header(alias))
            if header:
                mapping[canonical] = header
                break
    missing = sorted(REQUIRED_ORDER_FIELDS - set(mapping))
    known_headers = set(mapping.values())
    unknown = [header for header in headers if header not in known_headers]
    return mapping, missing, unknown


def parse_decimal(value: str | None) -> Decimal:
    if value is None or value.strip() == "":
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


def parse_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    clean = value.strip()
    for date_format in (
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
        "%d.%m.%Y %H:%M:%S",
        "%d.%m.%Y",
    ):
        try:
            parsed = datetime.strptime(clean, date_format)
            return parsed.replace(tzinfo=None)
        except ValueError:
            continue
    raise ValueError(f"Unsupported datetime value: {value}")


def normalize_fulfillment_channel(value: str | None) -> str:
    normalized = (value or "").strip().casefold()
    if normalized in {"amazon", "afn", "fba"}:
        return "FBA"
    if normalized in {"merchant", "mfn", "seller", "fbm"}:
        return "FBM"
    return "UNKNOWN"


def parse_order_row(row: dict[str, str], mapping: dict[str, str], marketplace: str) -> dict:
    return {
        "marketplace": marketplace,
        "amazon_order_id": (row.get(mapping["amazon_order_id"]) or "").strip(),
        "merchant_order_id": (row.get(mapping["merchant_order_id"]) or "").strip() or None if "merchant_order_id" in mapping else None,
        "purchase_date": parse_datetime(row.get(mapping["purchase_date"])),
        "last_updated_date": parse_datetime(row.get(mapping["last_updated_date"])) if "last_updated_date" in mapping else None,
        "order_status": (row.get(mapping["order_status"]) or "").strip() or None if "order_status" in mapping else None,
        "item_status": (row.get(mapping["item_status"]) or "").strip() or None if "item_status" in mapping else None,
        "fulfillment_channel": normalize_fulfillment_channel(row.get(mapping["fulfillment_channel"])),
        "sales_channel": (row.get(mapping["sales_channel"]) or "").strip() or None if "sales_channel" in mapping else None,
        "ship_service_level": (row.get(mapping["ship_service_level"]) or "").strip() or None if "ship_service_level" in mapping else None,
        "sku": (row.get(mapping["sku"]) or "").strip(),
        "asin": (row.get(mapping["asin"]) or "").strip() or None if "asin" in mapping else None,
        "product_name": (row.get(mapping["product_name"]) or "").strip() or None if "product_name" in mapping else None,
        "quantity": parse_decimal(row.get(mapping["quantity"])),
        "currency": (row.get(mapping["currency"]) or "").strip() or None if "currency" in mapping else None,
        "item_price": parse_decimal(row.get(mapping["item_price"])) if "item_price" in mapping else Decimal("0"),
        "item_tax": parse_decimal(row.get(mapping["item_tax"])) if "item_tax" in mapping else Decimal("0"),
        "shipping_price": parse_decimal(row.get(mapping["shipping_price"])) if "shipping_price" in mapping else Decimal("0"),
        "shipping_tax": parse_decimal(row.get(mapping["shipping_tax"])) if "shipping_tax" in mapping else Decimal("0"),
        "item_promotion_discount": parse_decimal(row.get(mapping["item_promotion_discount"])) if "item_promotion_discount" in mapping else Decimal("0"),
        "ship_promotion_discount": parse_decimal(row.get(mapping["ship_promotion_discount"])) if "ship_promotion_discount" in mapping else Decimal("0"),
        "raw_row": row,
    }


def build_order_report_preview(
    filename: str,
    content: bytes,
    marketplace: str,
    sample_size: int = 10,
) -> OrderReportPreview:
    text, encoding = decode_report(content)
    delimiter = detect_delimiter(text)
    reader = csv.DictReader(StringIO(text), delimiter=delimiter)
    headers = list(reader.fieldnames or [])
    mapping, missing_fields, unknown_headers = detect_mapping(headers)
    parsed_rows: list[dict] = []
    sample_rows: list[dict[str, str]] = []
    validation_errors: list[str] = []

    if missing_fields:
        return OrderReportPreview(
            filename=filename,
            encoding=encoding,
            delimiter=delimiter,
            headers=headers,
            mapping=mapping,
            missing_fields=missing_fields,
            unknown_headers=unknown_headers,
            row_count=0,
            parsed_rows=[],
            sample_rows=[],
            totals={"quantity": 0, "fba_quantity": 0, "fbm_quantity": 0, "orders": 0},
            validation_errors=[],
        )

    for row_number, row in enumerate(reader, start=2):
        normalized_row = {str(key or ""): str(value or "") for key, value in row.items()}
        try:
            parsed = parse_order_row(normalized_row, mapping, marketplace)
            if not parsed["amazon_order_id"] or not parsed["sku"]:
                continue
            parsed_rows.append(parsed)
            if len(sample_rows) < sample_size:
                sample_rows.append(normalized_row)
        except ValueError as exc:
            validation_errors.append(f"Row {row_number}: {exc}")

    quantity = sum((row["quantity"] for row in parsed_rows), Decimal("0"))
    fba_quantity = sum((row["quantity"] for row in parsed_rows if row["fulfillment_channel"] == "FBA"), Decimal("0"))
    fbm_quantity = sum((row["quantity"] for row in parsed_rows if row["fulfillment_channel"] == "FBM"), Decimal("0"))
    orders = len({row["amazon_order_id"] for row in parsed_rows})
    return OrderReportPreview(
        filename=filename,
        encoding=encoding,
        delimiter=delimiter,
        headers=headers,
        mapping=mapping,
        missing_fields=missing_fields,
        unknown_headers=unknown_headers,
        row_count=len(parsed_rows),
        parsed_rows=parsed_rows,
        sample_rows=sample_rows,
        totals={
            "quantity": float(quantity),
            "fba_quantity": float(fba_quantity),
            "fbm_quantity": float(fbm_quantity),
            "orders": orders,
        },
        validation_errors=validation_errors,
    )
