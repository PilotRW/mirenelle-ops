from unittest import TestCase

from app.ingestion.amazon_reports.storage_fee_reports import parse_storage_fees


class StorageFeeParserTest(TestCase):
    def test_maps_fnsku_to_seller_sku(self) -> None:
        content = (
            "asin\tfnsku\tproduct_name\tfulfillment_center\tcountry_code\t"
            "average_quantity_on_hand\testimated_total_item_volume\tmonth_of_charge\t"
            "currency\testimated_monthly_storage_fee\n"
            "A1\tF1\tProduct\tNUE1\tDE\t2\t0.003\t2026-05\tEUR\t1.25\n"
        ).encode()
        row = parse_storage_fees(content, {"F1": "SKU-1"})[0]
        self.assertEqual(row["sku"], "SKU-1")
        self.assertEqual(str(row["estimated_monthly_storage_fee"]), "1.25")
