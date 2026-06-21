"""add amazon returns

Revision ID: 20260621_0018
Revises: 20260619_0017
Create Date: 2026-06-21 18:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


revision: str = "20260621_0018"
down_revision: Union[str, None] = "20260619_0017"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "amazon_return_imports",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("source_filename", sa.String(length=255), nullable=False),
        sa.Column("source_sha256", sa.String(length=64), nullable=False),
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
    op.create_index(op.f("ix_amazon_return_imports_marketplace"), "amazon_return_imports", ["marketplace"], unique=False)

    op.create_table(
        "amazon_return_items",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("import_id", sa.Integer(), nullable=False),
        sa.Column("marketplace", sa.String(length=16), nullable=False),
        sa.Column("return_date", sa.DateTime(), nullable=False),
        sa.Column("order_id", sa.String(length=64), nullable=False),
        sa.Column("sku", sa.String(length=160), nullable=False),
        sa.Column("asin", sa.String(length=32), nullable=True),
        sa.Column("fnsku", sa.String(length=64), nullable=False),
        sa.Column("product_name", sa.Text(), nullable=True),
        sa.Column("quantity", sa.Numeric(12, 3), nullable=False),
        sa.Column("fulfillment_center_id", sa.String(length=32), nullable=True),
        sa.Column("detailed_disposition", sa.String(length=80), nullable=True),
        sa.Column("reason", sa.String(length=120), nullable=True),
        sa.Column("status", sa.String(length=160), nullable=True),
        sa.Column("license_plate_number", sa.String(length=120), nullable=False),
        sa.Column("customer_comments", sa.Text(), nullable=True),
        sa.Column("raw_row", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["import_id"], ["amazon_return_imports.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "order_id",
            "fnsku",
            "return_date",
            "license_plate_number",
            name="uq_amazon_return_items_order_fnsku_date_lpn",
        ),
    )
    for column in ("import_id", "marketplace", "return_date", "order_id", "sku", "asin", "fnsku"):
        op.create_index(op.f(f"ix_amazon_return_items_{column}"), "amazon_return_items", [column], unique=False)


def downgrade() -> None:
    for column in ("fnsku", "asin", "sku", "order_id", "return_date", "marketplace", "import_id"):
        op.drop_index(op.f(f"ix_amazon_return_items_{column}"), table_name="amazon_return_items")
    op.drop_table("amazon_return_items")
    op.drop_index(op.f("ix_amazon_return_imports_marketplace"), table_name="amazon_return_imports")
    op.drop_table("amazon_return_imports")
