from decimal import Decimal
from types import SimpleNamespace
from unittest import TestCase

from fastapi import HTTPException

from app.api.inventory import (
    bundle_component_sales,
    normalize_assembly_provider,
    split_bundle_component_consumption,
)


class BundleInventoryConsumptionTest(TestCase):
    def test_normalizes_supported_assembly_provider(self) -> None:
        self.assertEqual(
            normalize_assembly_provider(" Prep_Center "),
            "prep_center",
        )

    def test_rejects_unknown_assembly_provider_value(self) -> None:
        with self.assertRaises(HTTPException) as context:
            normalize_assembly_provider("warehouse")

        self.assertEqual(context.exception.status_code, 422)

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

    def test_component_snapshot_dict_is_supported(self) -> None:
        recipe = [
            {"component_sku": "MASK-A", "component_quantity": "2"},
        ]
        purchased = {
            "MASK-A": {"ean": "EAN-A"},
        }

        result = bundle_component_sales(recipe, Decimal("3"), purchased)

        self.assertEqual(result, {"MASK-A": Decimal("6")})

    def test_incomplete_recipe_does_not_partially_consume_inventory(self) -> None:
        recipe = [
            SimpleNamespace(component_sku="MASK-A", component_quantity=Decimal("1")),
            SimpleNamespace(component_sku="MISSING", component_quantity=Decimal("1")),
        ]
        purchased = {
            "MASK-A": {"ean": "EAN-A"},
        }

        self.assertIsNone(bundle_component_sales(recipe, Decimal("4"), purchased))

    def test_zero_quantity_is_valid_empty_consumption(self) -> None:
        recipe = [
            SimpleNamespace(component_sku="MASK-A", component_quantity=Decimal("1")),
        ]
        purchased = {
            "MASK-A": {"ean": "EAN-A"},
        }

        self.assertEqual(
            bundle_component_sales(recipe, Decimal("0"), purchased),
            {"MASK-A": Decimal("0")},
        )

    def test_recorded_assemblies_cover_bundle_sales_without_double_counting(self) -> None:
        uncovered_sales, assemblies = split_bundle_component_consumption(
            sold_quantity=Decimal("4"),
            assembly_quantity=Decimal("17"),
        )

        self.assertEqual(uncovered_sales, Decimal("0"))
        self.assertEqual(assemblies, Decimal("17"))

    def test_sales_without_assembly_still_consume_components(self) -> None:
        uncovered_sales, assemblies = split_bundle_component_consumption(
            sold_quantity=Decimal("4"),
            assembly_quantity=Decimal("0"),
        )

        self.assertEqual(uncovered_sales, Decimal("4"))
        self.assertEqual(assemblies, Decimal("0"))
