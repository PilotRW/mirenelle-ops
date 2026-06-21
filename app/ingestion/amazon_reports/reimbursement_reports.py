import csv
from datetime import datetime
from decimal import Decimal
from io import StringIO

REPORT_TYPE_REIMBURSEMENTS = "GET_FBA_REIMBURSEMENTS_DATA"


def parse_reimbursements(content: bytes) -> list[dict]:
    reader = csv.DictReader(StringIO(content.decode("utf-8-sig", errors="replace")), delimiter="\t")
    rows = []
    for raw in reader:
        row = {(k or "").strip(): (v or "").strip() for k, v in raw.items()}
        if not row.get("reimbursement-id") or not row.get("sku"):
            continue
        rows.append({
            "reimbursement_id": row["reimbursement-id"],
            "approval_date": datetime.fromisoformat(row["approval-date"].replace("Z", "+00:00")).replace(tzinfo=None),
            "amazon_order_id": row.get("amazon-order-id") or None,
            "reason": row.get("reason") or None,
            "sku": row["sku"],
            "fnsku": row.get("fnsku") or None,
            "asin": row.get("asin") or None,
            "product_name": row.get("product-name") or None,
            "currency": row.get("currency-unit") or "EUR",
            "amount_total": Decimal(row.get("amount-total") or "0"),
            "quantity_cash": Decimal(row.get("quantity-reimbursed-cash") or "0"),
            "quantity_inventory": Decimal(row.get("quantity-reimbursed-inventory") or "0"),
            "quantity_total": Decimal(row.get("quantity-reimbursed-total") or "0"),
            "raw_row": row,
        })
    return rows
