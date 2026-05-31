"""add import hashes and product costs

Revision ID: 20260529_0002
Revises: 20260529_0001
Create Date: 2026-05-29
"""

from typing import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


revision: str = "20260529_0002"
down_revision: str | None = "20260529_0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "amazon_payment_imports",
        sa.Column("source_sha256", sa.String(length=64), nullable=True),
    )
    op.create_unique_constraint(
        "uq_amazon_payment_imports_source_sha256",
        "amazon_payment_imports",
        ["source_sha256"],
    )

    op.create_table(
        "product_cost_imports",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("source_filename", sa.String(length=255), nullable=False),
        sa.Column("source_sha256", sa.String(length=64), nullable=True),
        sa.Column("currency", sa.String(length=8), nullable=False),
        sa.Column("effective_date", sa.Date(), nullable=False),
        sa.Column("header_mapping", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("row_count", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("source_sha256", name="uq_product_cost_imports_source_sha256"),
    )

    op.create_table(
        "product_costs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("import_id", sa.Integer(), nullable=False),
        sa.Column("sku", sa.String(length=120), nullable=False),
        sa.Column("product_name", sa.Text(), nullable=True),
        sa.Column("purchase_cost", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("currency", sa.String(length=8), nullable=False),
        sa.Column("effective_date", sa.Date(), nullable=False),
        sa.Column("raw_row", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["import_id"], ["product_cost_imports.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_product_costs_currency"), "product_costs", ["currency"], unique=False)
    op.create_index(op.f("ix_product_costs_effective_date"), "product_costs", ["effective_date"], unique=False)
    op.create_index(op.f("ix_product_costs_import_id"), "product_costs", ["import_id"], unique=False)
    op.create_index(op.f("ix_product_costs_sku"), "product_costs", ["sku"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_product_costs_sku"), table_name="product_costs")
    op.drop_index(op.f("ix_product_costs_import_id"), table_name="product_costs")
    op.drop_index(op.f("ix_product_costs_effective_date"), table_name="product_costs")
    op.drop_index(op.f("ix_product_costs_currency"), table_name="product_costs")
    op.drop_table("product_costs")
    op.drop_table("product_cost_imports")
    op.drop_constraint(
        "uq_amazon_payment_imports_source_sha256",
        "amazon_payment_imports",
        type_="unique",
    )
    op.drop_column("amazon_payment_imports", "source_sha256")
