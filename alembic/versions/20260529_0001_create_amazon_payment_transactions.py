"""create amazon payment transactions

Revision ID: 20260529_0001
Revises:
Create Date: 2026-05-29
"""

from typing import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


revision: str = "20260529_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "amazon_payment_imports",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("source_filename", sa.String(length=255), nullable=False),
        sa.Column("marketplace", sa.String(length=16), nullable=False),
        sa.Column("report_period_start", sa.DateTime(), nullable=True),
        sa.Column("report_period_end", sa.DateTime(), nullable=True),
        sa.Column("detected_locale", sa.String(length=16), nullable=True),
        sa.Column("header_mapping", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("row_count", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_amazon_payment_imports_marketplace"),
        "amazon_payment_imports",
        ["marketplace"],
        unique=False,
    )

    op.create_table(
        "amazon_payment_transaction_raw",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("import_id", sa.Integer(), nullable=False),
        sa.Column("row_number", sa.Integer(), nullable=False),
        sa.Column("raw_row", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["import_id"], ["amazon_payment_imports.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_amazon_payment_transaction_raw_import_id"),
        "amazon_payment_transaction_raw",
        ["import_id"],
        unique=False,
    )

    op.create_table(
        "amazon_payment_transactions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("import_id", sa.Integer(), nullable=False),
        sa.Column("raw_row_id", sa.Integer(), nullable=False),
        sa.Column("marketplace", sa.String(length=16), nullable=False),
        sa.Column("currency", sa.String(length=8), nullable=False),
        sa.Column("transaction_date", sa.Date(), nullable=False),
        sa.Column("transaction_status", sa.String(length=120), nullable=False),
        sa.Column("transaction_type", sa.String(length=160), nullable=False),
        sa.Column("external_transaction_id", sa.String(length=64), nullable=True),
        sa.Column("product_details", sa.Text(), nullable=True),
        sa.Column("product_charges", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("promotional_rebates", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("amazon_fees", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("other_amount", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("total_amount", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("raw_row", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["import_id"], ["amazon_payment_imports.id"]),
        sa.ForeignKeyConstraint(["raw_row_id"], ["amazon_payment_transaction_raw.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_amazon_payment_transactions_currency"),
        "amazon_payment_transactions",
        ["currency"],
        unique=False,
    )
    op.create_index(
        op.f("ix_amazon_payment_transactions_external_transaction_id"),
        "amazon_payment_transactions",
        ["external_transaction_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_amazon_payment_transactions_import_id"),
        "amazon_payment_transactions",
        ["import_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_amazon_payment_transactions_marketplace"),
        "amazon_payment_transactions",
        ["marketplace"],
        unique=False,
    )
    op.create_index(
        op.f("ix_amazon_payment_transactions_raw_row_id"),
        "amazon_payment_transactions",
        ["raw_row_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_amazon_payment_transactions_transaction_date"),
        "amazon_payment_transactions",
        ["transaction_date"],
        unique=False,
    )
    op.create_index(
        op.f("ix_amazon_payment_transactions_transaction_type"),
        "amazon_payment_transactions",
        ["transaction_type"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_amazon_payment_transactions_transaction_type"), table_name="amazon_payment_transactions")
    op.drop_index(op.f("ix_amazon_payment_transactions_transaction_date"), table_name="amazon_payment_transactions")
    op.drop_index(op.f("ix_amazon_payment_transactions_raw_row_id"), table_name="amazon_payment_transactions")
    op.drop_index(op.f("ix_amazon_payment_transactions_marketplace"), table_name="amazon_payment_transactions")
    op.drop_index(op.f("ix_amazon_payment_transactions_import_id"), table_name="amazon_payment_transactions")
    op.drop_index(op.f("ix_amazon_payment_transactions_external_transaction_id"), table_name="amazon_payment_transactions")
    op.drop_index(op.f("ix_amazon_payment_transactions_currency"), table_name="amazon_payment_transactions")
    op.drop_table("amazon_payment_transactions")
    op.drop_index(op.f("ix_amazon_payment_transaction_raw_import_id"), table_name="amazon_payment_transaction_raw")
    op.drop_table("amazon_payment_transaction_raw")
    op.drop_index(op.f("ix_amazon_payment_imports_marketplace"), table_name="amazon_payment_imports")
    op.drop_table("amazon_payment_imports")

