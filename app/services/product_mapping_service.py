import re
from dataclasses import dataclass
from decimal import Decimal
from difflib import SequenceMatcher

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.amazon_payment_transaction import AmazonPaymentTransaction
from app.models.product_mapping import ProductMapping
from app.models.purchase_invoice import PurchaseInvoice
from app.models.purchase_invoice_line import PurchaseInvoiceLine


def normalize_product_text(value: str | None) -> str:
    if not value:
        return ""
    normalized = value.casefold()
    normalized = re.sub(r"[^a-z0-9а-яіїєґąćęłńóśźżäöüß]+", " ", normalized)
    return re.sub(r"\s+", " ", normalized).strip()


def product_similarity(left: str | None, right: str | None) -> Decimal:
    left_norm = normalize_product_text(left)
    right_norm = normalize_product_text(right)
    if not left_norm or not right_norm:
        return Decimal("0")

    sequence_score = SequenceMatcher(None, left_norm, right_norm).ratio()
    left_tokens = set(left_norm.split())
    right_tokens = set(right_norm.split())
    token_score = len(left_tokens & right_tokens) / len(left_tokens | right_tokens) if left_tokens and right_tokens else 0
    score = (sequence_score * 0.65) + (token_score * 0.35)
    return Decimal(str(round(score * 100, 2)))


@dataclass(frozen=True)
class ProductMappingSuggestion:
    invoice_line_id: int
    invoice_product_name: str
    supplier_name: str
    supplier_sku: str | None
    sku: str | None
    ean: str | None
    amazon_product_details: str
    transaction_rows: int
    confidence: Decimal


async def create_product_mapping(
    db: AsyncSession,
    invoice_line_id: int,
    amazon_product_details: str,
    confidence: Decimal | None = None,
    match_method: str = "manual",
    notes: str | None = None,
    raw_match: dict | None = None,
) -> ProductMapping:
    line_result = await db.execute(
        select(PurchaseInvoiceLine, PurchaseInvoice)
        .join(PurchaseInvoice, PurchaseInvoice.id == PurchaseInvoiceLine.invoice_id)
        .where(PurchaseInvoiceLine.id == invoice_line_id)
    )
    row = line_result.first()
    if row is None:
        raise ValueError("Invoice line was not found.")

    line, invoice = row
    mapping = ProductMapping(
        invoice_line_id=line.id,
        amazon_product_details=amazon_product_details.strip(),
        supplier_name=invoice.supplier_name,
        supplier_sku=line.supplier_sku,
        sku=line.sku,
        ean=line.ean,
        invoice_product_name=line.product_name,
        confidence=confidence,
        match_method=match_method,
        notes=notes,
        raw_match=raw_match or {},
    )
    db.add(mapping)
    await db.commit()
    await db.refresh(mapping)
    return mapping


async def build_product_mapping_suggestions(
    db: AsyncSession,
    limit: int = 50,
    min_confidence: Decimal = Decimal("35"),
) -> list[ProductMappingSuggestion]:
    mapped_line_ids = select(ProductMapping.invoice_line_id)
    invoice_lines = await db.execute(
        select(PurchaseInvoiceLine, PurchaseInvoice)
        .join(PurchaseInvoice, PurchaseInvoice.id == PurchaseInvoiceLine.invoice_id)
        .where(PurchaseInvoiceLine.id.not_in(mapped_line_ids))
        .order_by(PurchaseInvoiceLine.created_at.desc(), PurchaseInvoiceLine.id.desc())
        .limit(500)
    )
    products = await db.execute(
        select(
            AmazonPaymentTransaction.product_details,
            func.count().label("transaction_rows"),
        )
        .where(AmazonPaymentTransaction.product_details.is_not(None))
        .where(AmazonPaymentTransaction.product_details != "")
        .group_by(AmazonPaymentTransaction.product_details)
    )
    product_rows = [
        (str(row.product_details), int(row.transaction_rows))
        for row in products
    ]

    suggestions: list[ProductMappingSuggestion] = []
    for line, invoice in invoice_lines:
        best_product = None
        best_rows = 0
        best_score = Decimal("0")
        for product_details, transaction_rows in product_rows:
            score = product_similarity(line.product_name, product_details)
            if score > best_score:
                best_product = product_details
                best_rows = transaction_rows
                best_score = score
        if best_product and best_score >= min_confidence:
            suggestions.append(
                ProductMappingSuggestion(
                    invoice_line_id=line.id,
                    invoice_product_name=line.product_name,
                    supplier_name=invoice.supplier_name,
                    supplier_sku=line.supplier_sku,
                    sku=line.sku,
                    ean=line.ean,
                    amazon_product_details=best_product,
                    transaction_rows=best_rows,
                    confidence=best_score,
                )
            )

    suggestions.sort(key=lambda item: item.confidence, reverse=True)
    return suggestions[:limit]
