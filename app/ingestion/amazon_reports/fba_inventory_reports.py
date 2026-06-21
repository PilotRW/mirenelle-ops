import csv
from datetime import datetime
from decimal import Decimal, InvalidOperation
from io import StringIO


REPORT_TYPE_FBA_INVENTORY = "GET_FBA_MYI_UNSUPPRESSED_INVENTORY_DATA"


def _decimal(value: str | None) -> Decimal:
    try:
        return Decimal((value or "0").strip().replace(",", ".") or "0")
    except InvalidOperation:
        return Decimal("0")


def parse_fba_inventory_report(content: bytes, marketplace: str, captured_at: datetime) -> list[dict]:
    text = content.decode("utf-8-sig", errors="replace")
    reader = csv.DictReader(StringIO(text), delimiter="\t")
    required = {"sku", "fnsku", "afn-fulfillable-quantity", "afn-reserved-quantity"}
    headers = set(reader.fieldnames or [])
    missing = required - headers
    if missing:
        raise ValueError(f"FBA inventory report is missing fields: {sorted(missing)}")
    rows: list[dict] = []
    for row in reader:
        clean = {(key or "").strip(): (value or "").strip() for key, value in row.items()}
        if not clean.get("sku") or not clean.get("fnsku"):
            continue
        rows.append(
            {
                "captured_at": captured_at,
                "marketplace": marketplace,
                "sku": clean["sku"],
                "fnsku": clean["fnsku"],
                "asin": clean.get("asin") or None,
                "product_name": clean.get("product-name") or None,
                "condition": clean.get("condition") or None,
                "fulfillable_quantity": _decimal(clean.get("afn-fulfillable-quantity")),
                "warehouse_quantity": _decimal(clean.get("afn-warehouse-quantity")),
                "unsellable_quantity": _decimal(clean.get("afn-unsellable-quantity")),
                "reserved_quantity": _decimal(clean.get("afn-reserved-quantity")),
                "total_quantity": _decimal(clean.get("afn-total-quantity")),
                "inbound_working_quantity": _decimal(clean.get("afn-inbound-working-quantity")),
                "inbound_shipped_quantity": _decimal(clean.get("afn-inbound-shipped-quantity")),
                "inbound_receiving_quantity": _decimal(clean.get("afn-inbound-receiving-quantity")),
                "researching_quantity": _decimal(clean.get("afn-researching-quantity")),
                "raw_row": clean,
            }
        )
    return rows
