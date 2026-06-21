from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.amazon_order_item import AmazonOrderItem
from app.models.amazon_payment_transaction import AmazonPaymentTransaction
from app.models.bundle_assembly import BundleAssembly
from app.services.fx import get_fx_rate_history, get_rate_on_date
from app.services.order_item_policy import partition_order_item_keys
from app.services.transaction_classifier import is_order_payment


@dataclass
class BundleAssemblyEventCost:
    units: Decimal = Decimal("0")
    cost_eur: Decimal = Decimal("0")


def _clean(value: str | None) -> str:
    return (value or "").strip()


def consume_bundle_assembly_lots(
    assemblies: list[BundleAssembly],
    remaining: dict[int, Decimal],
    sale_date: date,
    quantity: Decimal,
    rate_by_id: dict[int, Decimal],
) -> BundleAssemblyEventCost:
    result = BundleAssemblyEventCost()
    quantity_to_cost = abs(quantity)
    for assembly in assemblies:
        if quantity_to_cost <= 0:
            break
        if assembly.assembly_date > sale_date:
            continue
        available = remaining.get(assembly.id, Decimal("0"))
        if available <= 0:
            continue
        consumed = min(available, quantity_to_cost)
        result.units += consumed
        result.cost_eur += (
            consumed
            * Decimal(str(assembly.unit_assembly_cost or 0))
            * rate_by_id.get(assembly.id, Decimal("1"))
        )
        remaining[assembly.id] = available - consumed
        quantity_to_cost -= consumed
    result.cost_eur = result.cost_eur.quantize(Decimal("0.01"))
    return result


async def bundle_assembly_event_costs(
    db: AsyncSession,
    end_date: date | None,
) -> dict[tuple[str, str], BundleAssemblyEventCost]:
    fx_history = await get_fx_rate_history(db)
    assemblies = list(
        await db.scalars(
            select(BundleAssembly).order_by(
                BundleAssembly.assembly_date,
                BundleAssembly.id,
            )
        )
    )
    assemblies_by_sku: dict[str, list[BundleAssembly]] = defaultdict(list)
    for assembly in assemblies:
        assemblies_by_sku[_clean(assembly.bundle_sku)].append(assembly)
    remaining = {
        assembly.id: Decimal(str(assembly.quantity))
        for assembly in assemblies
    }
    rate_by_id = {
        assembly.id: Decimal(
            str(
                get_rate_on_date(
                    fx_history,
                    assembly.currency,
                    assembly.assembly_date,
                )
            )
        )
        for assembly in assemblies
    }

    sales_query = (
        select(AmazonPaymentTransaction)
        .where(AmazonPaymentTransaction.sku.is_not(None))
        .where(AmazonPaymentTransaction.quantity.is_not(None))
        .order_by(
            AmazonPaymentTransaction.transaction_date,
            AmazonPaymentTransaction.id,
        )
    )
    if end_date:
        sales_query = sales_query.where(
            AmazonPaymentTransaction.transaction_date <= end_date
        )
    order_items = list(await db.scalars(select(AmazonOrderItem)))
    known_order_keys, eligible_order_keys = partition_order_item_keys(order_items)
    event_costs: dict[tuple[str, str], BundleAssemblyEventCost] = {}
    processed_events: set[tuple[str, str]] = set()
    for sale in await db.scalars(sales_query):
        if not is_order_payment(sale.transaction_type):
            continue
        event_key = (
            _clean(sale.external_transaction_id),
            _clean(sale.sku),
        )
        if event_key in processed_events:
            continue
        if event_key in known_order_keys and event_key not in eligible_order_keys:
            continue
        matching_assemblies = assemblies_by_sku.get(event_key[1], [])
        if not matching_assemblies:
            continue
        processed_events.add(event_key)
        event_costs[event_key] = consume_bundle_assembly_lots(
            assemblies=matching_assemblies,
            remaining=remaining,
            sale_date=sale.transaction_date,
            quantity=Decimal(str(sale.quantity or 0)),
            rate_by_id=rate_by_id,
        )
    return event_costs
