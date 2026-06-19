from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.amazon_payment_transaction import AmazonPaymentTransaction
from app.models.bundle_component import BundleComponent
from app.models.inventory_lot import InventoryLot
from app.models.product_mapping import ProductMapping
from app.services.fx import get_fx_rate_history, get_rate_on_date
from app.services.product_mapping_service import product_similarity
from app.services.transaction_classifier import is_order_payment


@dataclass
class FifoEventCost:
    units: Decimal = Decimal("0")
    cogs_eur: Decimal = Decimal("0")


def consume_fifo_lots(
    matching_lots: list[InventoryLot],
    remaining: dict[int, Decimal],
    sale_date: date,
    quantity: Decimal,
    rate_by_currency: dict[str, Decimal],
) -> FifoEventCost:
    result = FifoEventCost()
    quantity_to_cost = abs(quantity)
    for lot in matching_lots:
        if quantity_to_cost <= 0:
            break
        if lot.purchase_date > sale_date:
            continue
        available = remaining.get(lot.id, Decimal("0"))
        if available <= 0:
            continue
        consumed = min(available, quantity_to_cost)
        rate = rate_by_currency.get(
            f"{lot.currency}:{lot.purchase_date.isoformat()}",
            Decimal("1"),
        )
        result.units += consumed
        result.cogs_eur += consumed * Decimal(str(lot.unit_cost)) * rate
        remaining[lot.id] = available - consumed
        quantity_to_cost -= consumed
    result.cogs_eur = result.cogs_eur.quantize(Decimal("0.01"))
    return result


def _clean(value: str | None) -> str:
    return (value or "").strip()


async def fifo_event_costs(
    db: AsyncSession,
    end_date: date | None,
) -> dict[tuple[str, str], FifoEventCost]:
    fx_history = await get_fx_rate_history(db)
    lots = list(
        await db.scalars(
            select(InventoryLot).order_by(
                InventoryLot.purchase_date,
                InventoryLot.id,
            )
        )
    )
    mappings = list(await db.scalars(select(ProductMapping).order_by(ProductMapping.id.desc())))
    bundle_components = list(
        await db.scalars(
            select(BundleComponent).order_by(
                BundleComponent.bundle_sku,
                BundleComponent.component_sku,
            )
        )
    )
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
        sales_query = sales_query.where(AmazonPaymentTransaction.transaction_date <= end_date)
    sales = [
        row
        for row in await db.scalars(sales_query)
        if is_order_payment(row.transaction_type)
    ]
    sale_aliases_by_sku: dict[str, set[str]] = defaultdict(set)
    for sale in sales:
        if sale.sku and sale.product_details:
            sale_aliases_by_sku[_clean(sale.sku)].add(_clean(sale.product_details))

    remaining = {
        lot.id: Decimal(str(lot.quantity_received))
        for lot in lots
    }
    rate_by_currency = {
        f"{lot.currency}:{lot.purchase_date.isoformat()}": Decimal(
            str(get_rate_on_date(fx_history, lot.currency, lot.purchase_date))
        )
        for lot in lots
    }
    mapping_by_product: dict[str, list[ProductMapping]] = defaultdict(list)
    for mapping in mappings:
        mapping_by_product[mapping.amazon_product_details].append(mapping)
    recipe_by_bundle: dict[str, list[BundleComponent]] = defaultdict(list)
    for component in bundle_components:
        recipe_by_bundle[_clean(component.bundle_sku)].append(component)

    match_cache: dict[tuple[str, str], list[InventoryLot]] = {}
    event_costs: dict[tuple[str, str], FifoEventCost] = {}

    for sale in sales:
        sale_sku = _clean(sale.sku)
        product_details = _clean(sale.product_details)
        recipe = recipe_by_bundle.get(sale_sku, [])
        if recipe:
            event_key = (_clean(sale.external_transaction_id), sale_sku)
            event = event_costs.setdefault(event_key, FifoEventCost())
            original_remaining = dict(remaining)
            recipe_cogs = Decimal("0")
            complete = True
            sale_quantity = abs(Decimal(str(sale.quantity or 0)))
            for component in recipe:
                component_sku = _clean(component.component_sku)
                component_lots = [
                    lot
                    for lot in lots
                    if component_sku
                    in {
                        _clean(lot.sku),
                        _clean(lot.supplier_sku),
                        _clean(lot.ean),
                    }
                ]
                required = sale_quantity * Decimal(str(component.component_quantity))
                consumed = consume_fifo_lots(
                    matching_lots=component_lots,
                    remaining=remaining,
                    sale_date=sale.transaction_date,
                    quantity=required,
                    rate_by_currency=rate_by_currency,
                )
                if consumed.units != required:
                    complete = False
                    break
                recipe_cogs += consumed.cogs_eur
            if complete:
                event.units += sale_quantity
                event.cogs_eur += recipe_cogs
            else:
                remaining = original_remaining
            continue

        cache_key = (sale_sku, product_details)
        matching_lots = match_cache.get(cache_key)
        if matching_lots is None:
            direct = [
                lot
                for lot in lots
                if sale_sku
                and sale_sku in {
                    _clean(lot.sku),
                    _clean(lot.supplier_sku),
                    _clean(lot.ean),
                }
            ]
            mapped: list[InventoryLot] = []
            if not direct:
                for mapping in mapping_by_product.get(product_details, []):
                    mapping_ids = {
                        _clean(mapping.sku),
                        _clean(mapping.supplier_sku),
                        _clean(mapping.ean),
                    }
                    mapped.extend(
                        lot
                        for lot in lots
                        if (
                            mapping_ids
                            & {
                                _clean(lot.sku),
                                _clean(lot.supplier_sku),
                                _clean(lot.ean),
                            }
                        )
                        or lot.product_name == mapping.invoice_product_name
                    )
            candidates = direct or mapped
            if not candidates and product_details:
                product_aliases = sale_aliases_by_sku.get(sale_sku, {product_details})
                candidates = [
                    lot
                    for lot in lots
                    if max(
                        (
                            product_similarity(alias, lot.product_name)
                            for alias in product_aliases
                        ),
                        default=Decimal("0"),
                    )
                    >= Decimal("55")
                ]
            matching_lots = sorted(
                {lot.id: lot for lot in candidates}.values(),
                key=lambda lot: (lot.purchase_date, lot.id),
            )
            match_cache[cache_key] = matching_lots

        event_key = (_clean(sale.external_transaction_id), sale_sku)
        event = event_costs.setdefault(event_key, FifoEventCost())
        consumed = consume_fifo_lots(
            matching_lots=matching_lots,
            remaining=remaining,
            sale_date=sale.transaction_date,
            quantity=Decimal(str(sale.quantity or 0)),
            rate_by_currency=rate_by_currency,
        )
        event.units += consumed.units
        event.cogs_eur += consumed.cogs_eur

    for event in event_costs.values():
        event.cogs_eur = event.cogs_eur.quantize(Decimal("0.01"))
    return event_costs
