from unittest import TestCase

from app.ingestion.amazon_reports.return_reports import build_return_report_preview


class ReturnReportParserTest(TestCase):
    def test_parses_customer_return_row(self) -> None:
        content = (
            "return-date\torder-id\tsku\tasin\tfnsku\tproduct-name\tquantity\t"
            "fulfillment-center-id\tdetailed-disposition\treason\tstatus\t"
            "license-plate-number\tcustomer-comments\n"
            "2026-05-28T09:01:50+00:00\tORDER-1\tSKU-1\tASIN-1\tFNSKU-1\t"
            "Product one\t1\tKTW1\tSELLABLE\tUNWANTED_ITEM\t"
            "Unit returned to inventory\tLPN-1\tComment\n"
        ).encode()
        preview = build_return_report_preview("returns.tsv", content, "EU")
        self.assertTrue(preview.can_commit)
        self.assertEqual(preview.row_count, 1)
        row = preview.parsed_rows[0]
        self.assertEqual(row["order_id"], "ORDER-1")
        self.assertEqual(row["sku"], "SKU-1")
        self.assertEqual(row["fnsku"], "FNSKU-1")
        self.assertEqual(str(row["quantity"]), "1")
        self.assertEqual(row["detailed_disposition"], "SELLABLE")
