from collections.abc import Iterable
from decimal import Decimal

from app.models.amazon_order_item import AmazonOrderItem


CANCELLED_STATUSES = {"cancelled", "canceled"}


def is_sellable_order_item(item: AmazonOrderItem) -> bool:
    marketplace = (item.marketplace or "").strip().upper()
    order_status = (item.order_status or "").strip().casefold()
    item_status = (item.item_status or "").strip().casefold()
    quantity = Decimal(str(item.quantity or 0))
    return (
        marketplace != "NON_AMAZON"
        and quantity > 0
        and order_status not in CANCELLED_STATUSES
        and item_status not in CANCELLED_STATUSES
    )


def order_item_key(item: AmazonOrderItem) -> tuple[str, str]:
    return (
        (item.amazon_order_id or "").strip(),
        (item.sku or "").strip(),
    )


def partition_order_item_keys(
    items: Iterable[AmazonOrderItem],
) -> tuple[set[tuple[str, str]], set[tuple[str, str]]]:
    known: set[tuple[str, str]] = set()
    eligible: set[tuple[str, str]] = set()
    for item in items:
        key = order_item_key(item)
        known.add(key)
        if is_sellable_order_item(item):
            eligible.add(key)
    return known, eligible
