from unittest import TestCase

from app.services.refund_reconciliation import (
    refund_match_status,
    refunded_skus_by_order,
    resolve_return_fee_sku,
)


class RefundReconciliationTest(TestCase):
    def test_refund_matches_exact_order_and_sku(self) -> None:
        status, units = refund_match_status(
            ("ORDER-1", "SKU-1"),
            {("ORDER-1", "SKU-1"): 2},
            1,
        )
        self.assertEqual((status, units), ("matched", 2))

    def test_refund_without_exact_sku_is_unmatched(self) -> None:
        status, units = refund_match_status(
            ("ORDER-1", "SKU-2"),
            {("ORDER-1", "SKU-1"): 1},
            1,
        )
        self.assertEqual((status, units), ("unmatched", None))

    def test_return_fee_links_single_refunded_sku(self) -> None:
        skus = refunded_skus_by_order([("ORDER-1", "SKU-1")])
        self.assertEqual(
            resolve_return_fee_sku("ORDER-1", skus),
            ("matched", "SKU-1"),
        )

    def test_return_fee_with_multiple_refunded_skus_is_ambiguous(self) -> None:
        skus = refunded_skus_by_order(
            [("ORDER-1", "SKU-1"), ("ORDER-1", "SKU-2")]
        )
        self.assertEqual(
            resolve_return_fee_sku("ORDER-1", skus),
            ("ambiguous", None),
        )
