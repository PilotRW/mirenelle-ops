from datetime import datetime
from unittest import TestCase

from app.ingestion.amazon_reports.fba_inventory_reports import parse_fba_inventory_report


class FbaInventoryParserTest(TestCase):
    def test_parses_quantities(self) -> None:
        content = (
            "sku\tfnsku\tasin\tproduct-name\tcondition\tafn-warehouse-quantity\t"
            "afn-fulfillable-quantity\tafn-unsellable-quantity\tafn-reserved-quantity\t"
            "afn-total-quantity\tafn-inbound-working-quantity\t"
            "afn-inbound-shipped-quantity\tafn-inbound-receiving-quantity\t"
            "afn-researching-quantity\n"
            "SKU-1\tFNSKU-1\tASIN-1\tProduct\tNew\t8\t5\t1\t2\t8\t1\t2\t3\t0\n"
        ).encode()
        rows = parse_fba_inventory_report(content, "EU", datetime(2026, 6, 21))
        self.assertEqual(len(rows), 1)
        self.assertEqual(str(rows[0]["fulfillable_quantity"]), "5")
        self.assertEqual(str(rows[0]["reserved_quantity"]), "2")
        self.assertEqual(str(rows[0]["inbound_receiving_quantity"]), "3")
