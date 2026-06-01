"""add supplier catalog items

Revision ID: 20260601_0008
Revises: 20260531_0007
Create Date: 2026-06-01 21:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


revision: str = "20260601_0008"
down_revision: Union[str, None] = "20260531_0007"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "supplier_catalog_items",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("source", sa.String(length=40), nullable=False),
        sa.Column("source_offer_id", sa.BigInteger(), nullable=False),
        sa.Column("supplier_name", sa.Text(), nullable=True),
        sa.Column("supplier_sku", sa.String(length=160), nullable=True),
        sa.Column("ean", sa.String(length=64), nullable=True),
        sa.Column("brand", sa.Text(), nullable=True),
        sa.Column("title", sa.Text(), nullable=True),
        sa.Column("cost", sa.Numeric(12, 2), nullable=True),
        sa.Column("currency", sa.String(length=8), nullable=True),
        sa.Column("source_imported_at", sa.DateTime(), nullable=True),
        sa.Column("raw_data", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("synced_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("source", "source_offer_id", name="uq_supplier_catalog_items_source_offer"),
    )
    op.create_index(op.f("ix_supplier_catalog_items_ean"), "supplier_catalog_items", ["ean"], unique=False)
    op.create_index(op.f("ix_supplier_catalog_items_source"), "supplier_catalog_items", ["source"], unique=False)
    op.create_index(op.f("ix_supplier_catalog_items_source_offer_id"), "supplier_catalog_items", ["source_offer_id"], unique=False)
    op.create_index(op.f("ix_supplier_catalog_items_supplier_name"), "supplier_catalog_items", ["supplier_name"], unique=False)
    op.create_index(op.f("ix_supplier_catalog_items_supplier_sku"), "supplier_catalog_items", ["supplier_sku"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_supplier_catalog_items_supplier_sku"), table_name="supplier_catalog_items")
    op.drop_index(op.f("ix_supplier_catalog_items_supplier_name"), table_name="supplier_catalog_items")
    op.drop_index(op.f("ix_supplier_catalog_items_source_offer_id"), table_name="supplier_catalog_items")
    op.drop_index(op.f("ix_supplier_catalog_items_source"), table_name="supplier_catalog_items")
    op.drop_index(op.f("ix_supplier_catalog_items_ean"), table_name="supplier_catalog_items")
    op.drop_table("supplier_catalog_items")
