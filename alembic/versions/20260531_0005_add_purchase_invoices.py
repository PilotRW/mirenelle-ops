"""add purchase invoices

Revision ID: 20260531_0005
Revises: 20260529_0004
Create Date: 2026-05-31
"""

from typing import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


revision: str = "20260531_0005"
down_revision: str | None = "20260529_0004"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "purchase_invoices",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("source_filename", sa.String(length=255), nullable=False),
        sa.Column("source_sha256", sa.String(length=64), nullable=True),
        sa.Column("supplier_name", sa.String(length=255), nullable=False),
        sa.Column("invoice_number", sa.String(length=120), nullable=True),
        sa.Column("invoice_date", sa.Date(), nullable=True),
        sa.Column("due_date", sa.Date(), nullable=True),
        sa.Column("currency", sa.String(length=8), nullable=False),
        sa.Column("subtotal_amount", sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column("vat_amount", sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column("total_amount", sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column("header_mapping", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("row_count", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("source_sha256", name="uq_purchase_invoices_source_sha256"),
    )
    op.create_index(op.f("ix_purchase_invoices_invoice_date"), "purchase_invoices", ["invoice_date"], unique=False)
    op.create_index(op.f("ix_purchase_invoices_invoice_number"), "purchase_invoices", ["invoice_number"], unique=False)
    op.create_index(op.f("ix_purchase_invoices_supplier_name"), "purchase_invoices", ["supplier_name"], unique=False)

    op.create_table(
        "purchase_invoice_lines",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("invoice_id", sa.Integer(), nullable=False),
        sa.Column("row_number", sa.Integer(), nullable=False),
        sa.Column("supplier_sku", sa.String(length=120), nullable=True),
        sa.Column("sku", sa.String(length=120), nullable=True),
        sa.Column("ean", sa.String(length=64), nullable=True),
        sa.Column("product_name", sa.Text(), nullable=False),
        sa.Column("quantity", sa.Numeric(precision=12, scale=3), nullable=False),
        sa.Column("unit_cost", sa.Numeric(precision=12, scale=4), nullable=False),
        sa.Column("line_net_amount", sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column("vat_rate_percent", sa.Numeric(precision=6, scale=2), nullable=True),
        sa.Column("vat_amount", sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column("line_gross_amount", sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column("currency", sa.String(length=8), nullable=False),
        sa.Column("raw_row", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["invoice_id"], ["purchase_invoices.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_purchase_invoice_lines_ean"), "purchase_invoice_lines", ["ean"], unique=False)
    op.create_index(op.f("ix_purchase_invoice_lines_invoice_id"), "purchase_invoice_lines", ["invoice_id"], unique=False)
    op.create_index(op.f("ix_purchase_invoice_lines_sku"), "purchase_invoice_lines", ["sku"], unique=False)
    op.create_index(op.f("ix_purchase_invoice_lines_supplier_sku"), "purchase_invoice_lines", ["supplier_sku"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_purchase_invoice_lines_supplier_sku"), table_name="purchase_invoice_lines")
    op.drop_index(op.f("ix_purchase_invoice_lines_sku"), table_name="purchase_invoice_lines")
    op.drop_index(op.f("ix_purchase_invoice_lines_invoice_id"), table_name="purchase_invoice_lines")
    op.drop_index(op.f("ix_purchase_invoice_lines_ean"), table_name="purchase_invoice_lines")
    op.drop_table("purchase_invoice_lines")
    op.drop_index(op.f("ix_purchase_invoices_supplier_name"), table_name="purchase_invoices")
    op.drop_index(op.f("ix_purchase_invoices_invoice_number"), table_name="purchase_invoices")
    op.drop_index(op.f("ix_purchase_invoices_invoice_date"), table_name="purchase_invoices")
    op.drop_table("purchase_invoices")

