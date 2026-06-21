from collections import defaultdict
from collections.abc import Iterable


def refund_match_status(
    order_key: tuple[str, str],
    sold_units_by_key: dict[tuple[str, str], float],
    refund_units: float,
) -> tuple[str, float | None]:
    sold_units = sold_units_by_key.get(order_key)
    if sold_units is None:
        return "unmatched", None
    if refund_units <= sold_units + 0.001:
        return "matched", sold_units
    return "quantity_mismatch", sold_units


def refunded_skus_by_order(
    refund_keys: Iterable[tuple[str, str]],
) -> dict[str, set[str]]:
    result: dict[str, set[str]] = defaultdict(set)
    for order_id, sku in refund_keys:
        if order_id and sku:
            result[order_id].add(sku)
    return dict(result)


def resolve_return_fee_sku(
    order_id: str,
    technical_sku: str,
    refunded_skus: dict[str, set[str]],
    returned_sku_by_order_fnsku: dict[tuple[str, str], str] | None = None,
) -> tuple[str, str | None]:
    exact_sku = (returned_sku_by_order_fnsku or {}).get((order_id, technical_sku))
    if exact_sku:
        return "matched", exact_sku
    candidates = refunded_skus.get(order_id, set())
    if len(candidates) == 1:
        return "matched", next(iter(candidates))
    if len(candidates) > 1:
        return "ambiguous", None
    return "unmatched", None
