from unittest import TestCase

from app.ingestion.amazon_reports.reimbursement_reports import parse_reimbursements


class ReimbursementParserTest(TestCase):
    def test_parses_reimbursement(self) -> None:
        content = (
            "approval-date\treimbursement-id\tamazon-order-id\treason\tsku\tfnsku\tasin\t"
            "product-name\tcurrency-unit\tamount-total\tquantity-reimbursed-cash\t"
            "quantity-reimbursed-inventory\tquantity-reimbursed-total\n"
            "2026-04-09T01:34:23+00:00\tR1\tO1\tCustomerReturn\tS1\tF1\tA1\t"
            "Product\tEUR\t93.84\t1\t0\t1\n"
        ).encode()
        row = parse_reimbursements(content)[0]
        self.assertEqual(row["reimbursement_id"], "R1")
        self.assertEqual(str(row["amount_total"]), "93.84")
