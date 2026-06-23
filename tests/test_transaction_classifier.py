from unittest import TestCase

from app.services.transaction_classifier import classify_payment_type


class TransactionClassifierTest(TestCase):
    def test_disbursement_is_transfer(self) -> None:
        self.assertEqual(classify_payment_type("Disbursement"), "transfer")

    def test_reimbursement_is_operating_reimbursement(self) -> None:
        self.assertEqual(
            classify_payment_type("REVERSAL_REIMBURSEMENT"),
            "reimbursement",
        )

    def test_localized_order_remains_order(self) -> None:
        self.assertEqual(classify_payment_type("Bestellung"), "order")
