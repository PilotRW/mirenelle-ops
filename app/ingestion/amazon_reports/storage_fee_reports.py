import csv
from datetime import date
from decimal import Decimal
from io import StringIO

REPORT_TYPE_STORAGE_FEES = "GET_FBA_STORAGE_FEE_CHARGES_DATA"


def parse_storage_fees(content: bytes, sku_by_fnsku: dict[str, str]) -> list[dict]:
    reader = csv.DictReader(StringIO(content.decode("utf-8-sig", errors="replace")), delimiter="\t")
    rows = []
    for raw in reader:
        row = {(k or "").strip(): (v or "").strip().strip("'") for k, v in raw.items()}
        if not row.get("fnsku") or not row.get("month_of_charge"):
            continue
        rows.append({
            "month_of_charge": date.fromisoformat(f"{row['month_of_charge']}-01"),
            "sku": sku_by_fnsku.get(row["fnsku"]),
            "fnsku": row["fnsku"],
            "asin": row.get("asin") or None,
            "product_name": row.get("product_name") or None,
            "fulfillment_center": row.get("fulfillment_center") or "",
            "country_code": row.get("country_code") or "",
            "average_quantity_on_hand": Decimal(row.get("average_quantity_on_hand") or "0"),
            "estimated_total_item_volume": Decimal(row.get("estimated_total_item_volume") or "0"),
            "currency": row.get("currency") or "EUR",
            "estimated_monthly_storage_fee": Decimal(row.get("estimated_monthly_storage_fee") or "0"),
            "raw_row": row,
        })
    return rows
