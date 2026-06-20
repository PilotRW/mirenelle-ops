from types import SimpleNamespace
from unittest import TestCase

from app.services.order_item_policy import (
    is_sellable_order_item,
    partition_order_item_keys,
)


def order_item(
    *,
    order_id: str = "ORDER-1",
    sku: str = "SKU-1",
    marketplace: str = "DE",
    quantity: float = 1,
    order_status: str = "Shipped",
    item_status: str = "Shipped",
) -> SimpleNamespace:
    return SimpleNamespace(
        amazon_order_id=order_id,
        sku=sku,
        marketplace=marketplace,
        quantity=quantity,
        order_status=order_status,
        item_status=item_status,
    )


class OrderItemPolicyTest(TestCase):
    def test_shipped_marketplace_order_is_sellable(self) -> None:
        self.assertTrue(is_sellable_order_item(order_item()))

    def test_non_amazon_order_is_not_sellable(self) -> None:
        self.assertFalse(
            is_sellable_order_item(
                order_item(marketplace="NON_AMAZON", quantity=6)
            )
        )

    def test_cancelled_or_zero_quantity_order_is_not_sellable(self) -> None:
        self.assertFalse(
            is_sellable_order_item(
                order_item(quantity=0, order_status="Cancelled", item_status="Cancelled")
            )
        )

    def test_key_is_eligible_when_any_matching_item_is_sellable(self) -> None:
        known, eligible = partition_order_item_keys(
            [
                order_item(quantity=0, order_status="Cancelled"),
                order_item(quantity=2, order_status="Shipped"),
            ]
        )
        self.assertEqual(known, {("ORDER-1", "SKU-1")})
        self.assertEqual(eligible, {("ORDER-1", "SKU-1")})
