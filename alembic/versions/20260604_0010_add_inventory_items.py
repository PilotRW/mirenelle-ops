"""add inventory items

Revision ID: 20260604_0010
Revises: 20260602_0009
Create Date: 2026-06-04 17:30:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


revision: str = "20260604_0010"
down_revision: Union[str, None] = "20260602_0009"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "inventory_items",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("sku", sa.String(length=160), nullable=False),
        sa.Column("ean", sa.String(length=64), nullable=True),
        sa.Column("asin", sa.String(length=32), nullable=True),
        sa.Column("product_name", sa.Text(), nullable=True),
        sa.Column("marketplace", sa.String(length=16), nullable=False),
        sa.Column("fulfillment_channel", sa.String(length=40), nullable=False),
        sa.Column("quantity_on_hand", sa.Numeric(12, 3), nullable=False),
        sa.Column("quantity_reserved", sa.Numeric(12, 3), nullable=False),
        sa.Column("quantity_inbound", sa.Numeric(12, 3), nullable=False),
        sa.Column("reorder_point", sa.Numeric(12, 3), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("sku", "marketplace", "fulfillment_channel", name="uq_inventory_items_sku_marketplace_channel"),
    )
    op.create_index(op.f("ix_inventory_items_asin"), "inventory_items", ["asin"], unique=False)
    op.create_index(op.f("ix_inventory_items_ean"), "inventory_items", ["ean"], unique=False)
    op.create_index(op.f("ix_inventory_items_fulfillment_channel"), "inventory_items", ["fulfillment_channel"], unique=False)
    op.create_index(op.f("ix_inventory_items_marketplace"), "inventory_items", ["marketplace"], unique=False)
    op.create_index(op.f("ix_inventory_items_sku"), "inventory_items", ["sku"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_inventory_items_sku"), table_name="inventory_items")
    op.drop_index(op.f("ix_inventory_items_marketplace"), table_name="inventory_items")
    op.drop_index(op.f("ix_inventory_items_fulfillment_channel"), table_name="inventory_items")
    op.drop_index(op.f("ix_inventory_items_ean"), table_name="inventory_items")
    op.drop_index(op.f("ix_inventory_items_asin"), table_name="inventory_items")
    op.drop_table("inventory_items")
