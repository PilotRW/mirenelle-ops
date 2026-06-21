"""add amazon reimbursements

Revision ID: 20260621_0020
Revises: 20260621_0019
"""
from typing import Sequence, Union
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260621_0020"
down_revision: Union[str, None] = "20260621_0019"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "amazon_reimbursements",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("reimbursement_id", sa.String(64), nullable=False),
        sa.Column("approval_date", sa.DateTime(), nullable=False),
        sa.Column("amazon_order_id", sa.String(64), nullable=True),
        sa.Column("reason", sa.String(120), nullable=True),
        sa.Column("sku", sa.String(160), nullable=False),
        sa.Column("fnsku", sa.String(64), nullable=True),
        sa.Column("asin", sa.String(32), nullable=True),
        sa.Column("product_name", sa.Text(), nullable=True),
        sa.Column("currency", sa.String(8), nullable=False),
        sa.Column("amount_total", sa.Numeric(12, 2), nullable=False),
        sa.Column("quantity_cash", sa.Numeric(12, 3), nullable=False),
        sa.Column("quantity_inventory", sa.Numeric(12, 3), nullable=False),
        sa.Column("quantity_total", sa.Numeric(12, 3), nullable=False),
        sa.Column("raw_row", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("reimbursement_id"),
    )
    for column in ("approval_date", "amazon_order_id", "sku", "fnsku", "asin"):
        op.create_index(op.f(f"ix_amazon_reimbursements_{column}"), "amazon_reimbursements", [column], unique=False)


def downgrade() -> None:
    for column in ("asin", "fnsku", "sku", "amazon_order_id", "approval_date"):
        op.drop_index(op.f(f"ix_amazon_reimbursements_{column}"), table_name="amazon_reimbursements")
    op.drop_table("amazon_reimbursements")
