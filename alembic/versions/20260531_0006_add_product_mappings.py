"""add product mappings

Revision ID: 20260531_0006
Revises: 20260531_0005
Create Date: 2026-05-31 16:30:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


revision: str = "20260531_0006"
down_revision: Union[str, None] = "20260531_0005"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "product_mappings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("invoice_line_id", sa.Integer(), nullable=False),
        sa.Column("amazon_product_details", sa.Text(), nullable=False),
        sa.Column("supplier_name", sa.String(length=255), nullable=True),
        sa.Column("supplier_sku", sa.String(length=120), nullable=True),
        sa.Column("sku", sa.String(length=120), nullable=True),
        sa.Column("ean", sa.String(length=64), nullable=True),
        sa.Column("invoice_product_name", sa.Text(), nullable=False),
        sa.Column("confidence", sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column("match_method", sa.String(length=40), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("raw_match", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["invoice_line_id"], ["purchase_invoice_lines.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "invoice_line_id",
            "amazon_product_details",
            name="uq_product_mappings_invoice_line_amazon_product",
        ),
    )
    op.create_index(op.f("ix_product_mappings_amazon_product_details"), "product_mappings", ["amazon_product_details"], unique=False)
    op.create_index(op.f("ix_product_mappings_ean"), "product_mappings", ["ean"], unique=False)
    op.create_index(op.f("ix_product_mappings_invoice_line_id"), "product_mappings", ["invoice_line_id"], unique=False)
    op.create_index(op.f("ix_product_mappings_sku"), "product_mappings", ["sku"], unique=False)
    op.create_index(op.f("ix_product_mappings_supplier_name"), "product_mappings", ["supplier_name"], unique=False)
    op.create_index(op.f("ix_product_mappings_supplier_sku"), "product_mappings", ["supplier_sku"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_product_mappings_supplier_sku"), table_name="product_mappings")
    op.drop_index(op.f("ix_product_mappings_supplier_name"), table_name="product_mappings")
    op.drop_index(op.f("ix_product_mappings_sku"), table_name="product_mappings")
    op.drop_index(op.f("ix_product_mappings_invoice_line_id"), table_name="product_mappings")
    op.drop_index(op.f("ix_product_mappings_ean"), table_name="product_mappings")
    op.drop_index(op.f("ix_product_mappings_amazon_product_details"), table_name="product_mappings")
    op.drop_table("product_mappings")
