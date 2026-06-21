from decimal import Decimal
from types import SimpleNamespace
from unittest import TestCase

from app.api.inventory import bundle_component_sales


class BundleInventoryConsumptionTest(TestCase):
    def test_expands_bundle_units_into_component_sales(self) -> None:
        recipe = [
            SimpleNamespace(component_sku="MASK-A", component_quantity=Decimal("1")),
            SimpleNamespace(component_sku="MASK-B", component_quantity=Decimal("2")),
        ]
        purchased = {
            "MASK-A": {"ean": "EAN-A"},
            "MASK-B": {"ean": "EAN-B"},
        }

        result = bundle_component_sales(recipe, Decimal("4"), purchased)

        self.assertEqual(
            result,
            {
                "MASK-A": Decimal("4"),
                "MASK-B": Decimal("8"),
            },
        )

    def test_component_ean_resolves_to_purchased_sku(self) -> None:
        recipe = [
            SimpleNamespace(component_sku="8800000000001", component_quantity=Decimal("1")),
        ]
        purchased = {
            "SUPPLIER-SKU": {"ean": "8800000000001"},
        }

        result = bundle_component_sales(recipe, Decimal("3"), purchased)

        self.assertEqual(result, {"SUPPLIER-SKU": Decimal("3")})

    def test_incomplete_recipe_does_not_partially_consume_inventory(self) -> None:
        recipe = [
            SimpleNamespace(component_sku="MASK-A", component_quantity=Decimal("1")),
            SimpleNamespace(component_sku="MISSING", component_quantity=Decimal("1")),
        ]
        purchased = {
            "MASK-A": {"ean": "EAN-A"},
        }

        self.assertIsNone(bundle_component_sales(recipe, Decimal("4"), purchased))
