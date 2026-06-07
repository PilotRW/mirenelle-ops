"""add amazon order reports

Revision ID: 20260607_0013
Revises: 20260607_0012
Create Date: 2026-06-07 11:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


revision: str = "20260607_0013"
down_revision: Union[str, None] = "20260607_0012"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "amazon_order_imports",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("source_filename", sa.String(length=255), nullable=False),
        sa.Column("source_sha256", sa.String(length=64), nullable=True),
        sa.Column("marketplace", sa.String(length=16), nullable=False),
        sa.Column("report_type", sa.String(length=120), nullable=False),
        sa.Column("report_period_start", sa.DateTime(), nullable=True),
        sa.Column("report_period_end", sa.DateTime(), nullable=True),
        sa.Column("header_mapping", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("row_count", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("source_sha256"),
    )
    op.create_index(op.f("ix_amazon_order_imports_marketplace"), "amazon_order_imports", ["marketplace"], unique=False)

    op.create_table(
        "amazon_order_items",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("import_id", sa.Integer(), nullable=False),
        sa.Column("marketplace", sa.String(length=16), nullable=False),
        sa.Column("amazon_order_id", sa.String(length=64), nullable=False),
        sa.Column("merchant_order_id", sa.String(length=64), nullable=True),
        sa.Column("purchase_date", sa.DateTime(), nullable=True),
        sa.Column("last_updated_date", sa.DateTime(), nullable=True),
        sa.Column("order_status", sa.String(length=80), nullable=True),
        sa.Column("item_status", sa.String(length=80), nullable=True),
        sa.Column("fulfillment_channel", sa.String(length=16), nullable=False),
        sa.Column("sales_channel", sa.String(length=80), nullable=True),
        sa.Column("ship_service_level", sa.String(length=120), nullable=True),
        sa.Column("sku", sa.String(length=160), nullable=False),
        sa.Column("asin", sa.String(length=32), nullable=True),
        sa.Column("product_name", sa.Text(), nullable=True),
        sa.Column("quantity", sa.Numeric(12, 3), nullable=False),
        sa.Column("currency", sa.String(length=8), nullable=True),
        sa.Column("item_price", sa.Numeric(12, 2), nullable=False),
        sa.Column("item_tax", sa.Numeric(12, 2), nullable=False),
        sa.Column("shipping_price", sa.Numeric(12, 2), nullable=False),
        sa.Column("shipping_tax", sa.Numeric(12, 2), nullable=False),
        sa.Column("item_promotion_discount", sa.Numeric(12, 2), nullable=False),
        sa.Column("ship_promotion_discount", sa.Numeric(12, 2), nullable=False),
        sa.Column("raw_row", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["import_id"], ["amazon_order_imports.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("amazon_order_id", "sku", "asin", "import_id", name="uq_amazon_order_items_order_sku_asin_import"),
    )
    for column in (
        "amazon_order_id",
        "asin",
        "currency",
        "fulfillment_channel",
        "import_id",
        "item_status",
        "marketplace",
        "merchant_order_id",
        "order_status",
        "purchase_date",
        "sku",
    ):
        op.create_index(op.f(f"ix_amazon_order_items_{column}"), "amazon_order_items", [column], unique=False)


def downgrade() -> None:
    for column in (
        "sku",
        "purchase_date",
        "order_status",
        "merchant_order_id",
        "marketplace",
        "item_status",
        "import_id",
        "fulfillment_channel",
        "currency",
        "asin",
        "amazon_order_id",
    ):
        op.drop_index(op.f(f"ix_amazon_order_items_{column}"), table_name="amazon_order_items")
    op.drop_table("amazon_order_items")
    op.drop_index(op.f("ix_amazon_order_imports_marketplace"), table_name="amazon_order_imports")
    op.drop_table("amazon_order_imports")
