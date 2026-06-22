from decimal import Decimal
from unittest import TestCase

from app.services.amazon_finances_sync_service import finance_transaction_rows


class AmazonFinancesSyncServiceTest(TestCase):
    def test_normalizes_shipment_item(self) -> None:
        rows = finance_transaction_rows(
            "SE",
            [
                {
                    "transactionType": "Shipment",
                    "transactionId": "TX-1",
                    "transactionStatus": "RELEASED",
                    "description": "Order Payment",
                    "postedDate": "2026-05-26T08:50:36Z",
                    "relatedIdentifiers": [
                        {
                            "relatedIdentifierName": "ORDER_ID",
                            "relatedIdentifierValue": "ORDER-1",
                        }
                    ],
                    "items": [
                        {
                            "description": "Product",
                            "totalAmount": {
                                "currencyAmount": 223.19,
                                "currencyCode": "SEK",
                            },
                            "breakdowns": [
                                {
                                    "breakdownType": "ProductCharges",
                                    "breakdownAmount": {
                                        "currencyAmount": 255.99,
                                        "currencyCode": "SEK",
                                    },
                                },
                                {
                                    "breakdownType": "Tax",
                                    "breakdownAmount": {
                                        "currencyAmount": 64,
                                        "currencyCode": "SEK",
                                    },
                                },
                                {
                                    "breakdownType": "AmazonFees",
                                    "breakdownAmount": {
                                        "currencyAmount": -96.8,
                                        "currencyCode": "SEK",
                                    },
                                },
                            ],
                            "contexts": [
                                {
                                    "contextType": "ProductContext",
                                    "sku": "SKU-1",
                                    "quantityShipped": 1,
                                    "fulfillmentNetwork": "AFN",
                                }
                            ],
                        }
                    ],
                }
            ],
        )

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["source_event_id"], "finances:SE:TX-1:0")
        self.assertEqual(rows[0]["external_transaction_id"], "ORDER-1")
        self.assertEqual(rows[0]["sku"], "SKU-1")
        self.assertEqual(rows[0]["quantity"], Decimal("1"))
        self.assertEqual(rows[0]["fulfillment_channel"], "FBA")
        self.assertEqual(rows[0]["product_charges"], Decimal("255.99"))
        self.assertEqual(rows[0]["amazon_fees"], Decimal("-96.8"))
        self.assertEqual(rows[0]["other_amount"], Decimal("0.00"))

    def test_transaction_without_items_becomes_single_ledger_row(self) -> None:
        rows = finance_transaction_rows(
            "DE",
            [
                {
                    "transactionType": "Transfer",
                    "transactionId": "TX-2",
                    "transactionStatus": "RELEASED",
                    "description": "Transfer",
                    "postedDate": "2026-05-30T10:00:00Z",
                    "totalAmount": {
                        "currencyAmount": -100,
                        "currencyCode": "EUR",
                    },
                    "items": [],
                    "breakdowns": [],
                }
            ],
        )

        self.assertEqual(len(rows), 1)
        self.assertIsNone(rows[0]["sku"])
        self.assertEqual(rows[0]["other_amount"], Decimal("-100"))
        self.assertEqual(rows[0]["total_amount"], Decimal("-100"))

    def test_deferred_and_released_lifecycle_is_deduplicated(self) -> None:
        base = {
            "transactionType": "Shipment",
            "description": "Order Payment",
            "items": [],
            "breakdowns": [],
            "totalAmount": {"currencyAmount": 10, "currencyCode": "EUR"},
        }
        rows = finance_transaction_rows(
            "IE",
            [
                {
                    **base,
                    "transactionId": "DEFERRED-ID",
                    "transactionStatus": "DEFERRED_RELEASED",
                    "postedDate": "2026-05-28T10:00:00Z",
                    "relatedIdentifiers": [
                        {
                            "relatedIdentifierName": "RELEASE_TRANSACTION_ID",
                            "relatedIdentifierValue": "RELEASE-ID",
                        }
                    ],
                },
                {
                    **base,
                    "transactionId": "RELEASE-ID",
                    "transactionStatus": "RELEASED",
                    "postedDate": "2026-06-07T10:00:00Z",
                },
            ],
        )

        self.assertEqual(len(rows), 1)
        self.assertEqual(
            rows[0]["source_event_id"],
            "finances:IE:RELEASE-ID:0",
        )
        self.assertEqual(rows[0]["transaction_status"], "RELEASED")
        self.assertEqual(rows[0]["transaction_date"].isoformat(), "2026-06-07")
