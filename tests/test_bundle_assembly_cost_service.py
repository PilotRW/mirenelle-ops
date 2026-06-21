from datetime import date
from decimal import Decimal
from types import SimpleNamespace
from unittest import TestCase

from app.services.bundle_assembly_cost_service import consume_bundle_assembly_lots


class BundleAssemblyCostServiceTest(TestCase):
    def test_consumes_assembly_cost_fifo_and_converts_currency(self) -> None:
        assemblies = [
            SimpleNamespace(
                id=1,
                assembly_date=date(2026, 5, 1),
                unit_assembly_cost=Decimal("0.50"),
            ),
            SimpleNamespace(
                id=2,
                assembly_date=date(2026, 6, 1),
                unit_assembly_cost=Decimal("0.80"),
            ),
        ]
        remaining = {1: Decimal("2"), 2: Decimal("3")}

        result = consume_bundle_assembly_lots(
            assemblies=assemblies,
            remaining=remaining,
            sale_date=date(2026, 6, 10),
            quantity=Decimal("4"),
            rate_by_id={1: Decimal("1"), 2: Decimal("1.25")},
        )

        self.assertEqual(result.units, Decimal("4"))
        self.assertEqual(result.cost_eur, Decimal("3.00"))
        self.assertEqual(remaining, {1: Decimal("0"), 2: Decimal("1")})

    def test_does_not_use_future_assembly(self) -> None:
        assembly = SimpleNamespace(
            id=1,
            assembly_date=date(2026, 6, 20),
            unit_assembly_cost=Decimal("1"),
        )

        result = consume_bundle_assembly_lots(
            assemblies=[assembly],
            remaining={1: Decimal("5")},
            sale_date=date(2026, 6, 10),
            quantity=Decimal("2"),
            rate_by_id={1: Decimal("1")},
        )

        self.assertEqual(result.units, Decimal("0"))
        self.assertEqual(result.cost_eur, Decimal("0.00"))
