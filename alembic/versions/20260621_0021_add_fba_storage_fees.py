"""add fba storage fees

Revision ID: 20260621_0021
Revises: 20260621_0020
"""
from typing import Sequence, Union
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260621_0021"
down_revision: Union[str, None] = "20260621_0020"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "fba_storage_fees",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("month_of_charge", sa.Date(), nullable=False),
        sa.Column("sku", sa.String(160), nullable=True),
        sa.Column("fnsku", sa.String(64), nullable=False),
        sa.Column("asin", sa.String(32), nullable=True),
        sa.Column("product_name", sa.Text(), nullable=True),
        sa.Column("fulfillment_center", sa.String(32), nullable=False),
        sa.Column("country_code", sa.String(8), nullable=False),
        sa.Column("average_quantity_on_hand", sa.Numeric(12, 3), nullable=False),
        sa.Column("estimated_total_item_volume", sa.Numeric(16, 6), nullable=False),
        sa.Column("currency", sa.String(8), nullable=False),
        sa.Column("estimated_monthly_storage_fee", sa.Numeric(12, 4), nullable=False),
        sa.Column("raw_row", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "month_of_charge", "fnsku", "fulfillment_center", "country_code",
            name="uq_fba_storage_fee_month_fnsku_center",
        ),
    )
    for column in ("month_of_charge", "sku", "fnsku", "asin"):
        op.create_index(op.f(f"ix_fba_storage_fees_{column}"), "fba_storage_fees", [column], unique=False)


def downgrade() -> None:
    for column in ("asin", "fnsku", "sku", "month_of_charge"):
        op.drop_index(op.f(f"ix_fba_storage_fees_{column}"), table_name="fba_storage_fees")
    op.drop_table("fba_storage_fees")
