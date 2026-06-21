from types import SimpleNamespace
from unittest import TestCase

from app.services.refund_reconciliation import (
    refund_only_period_costs,
    refund_product_key,
    refund_match_status,
    refunded_skus_by_order,
    resolve_return_fee_sku,
)


class RefundReconciliationTest(TestCase):
    def test_refund_only_period_has_zero_cogs_without_dividing_by_zero(self) -> None:
        self.assertEqual(
            refund_only_period_costs(
                units_estimated=0,
                fifo_units_costed=0,
                fifo_cogs_eur=0,
            ),
            (True, None, 0),
        )

    def test_prior_period_refund_creates_product_key_from_exact_order(self) -> None:
        order = SimpleNamespace(fulfillment_channel="FBA", currency="EUR")

        self.assertEqual(
            refund_product_key(
                linked_sku="SKU-1",
                row_fulfillment_channel="FBA",
                row_currency="EUR",
                matched_order=order,
                candidate_keys=[],
                existing_keys=set(),
            ),
            ("SKU-1", "FBA", "EUR"),
        )

    def test_unmatched_technical_fee_does_not_create_product_key(self) -> None:
        self.assertIsNone(
            refund_product_key(
                linked_sku="TECHNICAL-FEE-SKU",
                row_fulfillment_channel="FBA",
                row_currency="EUR",
                matched_order=None,
                candidate_keys=[],
                existing_keys=set(),
            )
        )

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
            resolve_return_fee_sku("ORDER-1", "FNSKU-1", skus),
            ("matched", "SKU-1"),
        )

    def test_return_fee_with_multiple_refunded_skus_is_ambiguous(self) -> None:
        skus = refunded_skus_by_order(
            [("ORDER-1", "SKU-1"), ("ORDER-1", "SKU-2")]
        )
        self.assertEqual(
            resolve_return_fee_sku("ORDER-1", "FNSKU-1", skus),
            ("ambiguous", None),
        )

    def test_return_report_fnsku_resolves_ambiguous_fee(self) -> None:
        skus = refunded_skus_by_order(
            [("ORDER-1", "SKU-1"), ("ORDER-1", "SKU-2")]
        )
        self.assertEqual(
            resolve_return_fee_sku(
                "ORDER-1",
                "FNSKU-2",
                skus,
                {("ORDER-1", "FNSKU-2"): "SKU-2"},
            ),
            ("matched", "SKU-2"),
        )
