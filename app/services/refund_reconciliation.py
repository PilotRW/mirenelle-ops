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


def refund_product_key(
    linked_sku: str,
    row_fulfillment_channel: str,
    row_currency: str,
    matched_order: object | None,
    candidate_keys: list[tuple[str, str, str]],
    existing_keys: set[tuple[str, str, str]],
) -> tuple[str, str, str] | None:
    preferred_key = None
    if matched_order:
        preferred_key = (
            linked_sku,
            str(getattr(matched_order, "fulfillment_channel", "") or row_fulfillment_channel),
            str(getattr(matched_order, "currency", "") or row_currency),
        )
        # An exact Order ID + SKU match is authoritative even if the original
        # sale was outside the selected profitability period.
        return preferred_key
    preferred_key = next(
        (
            key
            for key in candidate_keys
            if key[1] == row_fulfillment_channel and key[2] == row_currency
        ),
        candidate_keys[0] if len(candidate_keys) == 1 else None,
    )
    return preferred_key if preferred_key in existing_keys else None


def refund_only_period_costs(
    units_estimated: int,
    fifo_units_costed: float,
    fifo_cogs_eur: float,
) -> tuple[bool, float | None, float | None]:
    has_complete_cost = (
        units_estimated == 0
        or abs(fifo_units_costed - units_estimated) <= 0.001
    )
    purchase_cost_eur = (
        round(fifo_cogs_eur / units_estimated, 2)
        if has_complete_cost and units_estimated > 0
        else None
    )
    cogs_eur = fifo_cogs_eur if has_complete_cost else None
    return has_complete_cost, purchase_cost_eur, cogs_eur
