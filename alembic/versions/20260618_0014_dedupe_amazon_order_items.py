"""dedupe amazon order items across overlapping reports

Revision ID: 20260618_0014
Revises: 20260607_0013
Create Date: 2026-06-18 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


revision: str = "20260618_0014"
down_revision: Union[str, None] = "20260607_0013"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint(
        "uq_amazon_order_items_order_sku_asin_import",
        "amazon_order_items",
        type_="unique",
    )
    op.create_unique_constraint(
        "uq_amazon_order_items_order_sku_asin",
        "amazon_order_items",
        ["amazon_order_id", "sku", "asin"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "uq_amazon_order_items_order_sku_asin",
        "amazon_order_items",
        type_="unique",
    )
    op.create_unique_constraint(
        "uq_amazon_order_items_order_sku_asin_import",
        "amazon_order_items",
        ["amazon_order_id", "sku", "asin", "import_id"],
    )
