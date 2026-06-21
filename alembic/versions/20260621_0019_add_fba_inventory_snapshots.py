"""add fba inventory snapshots

Revision ID: 20260621_0019
Revises: 20260621_0018
Create Date: 2026-06-21 19:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


revision: str = "20260621_0019"
down_revision: Union[str, None] = "20260621_0018"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "fba_inventory_snapshots",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("captured_at", sa.DateTime(), nullable=False),
        sa.Column("marketplace", sa.String(length=16), nullable=False),
        sa.Column("sku", sa.String(length=160), nullable=False),
        sa.Column("fnsku", sa.String(length=64), nullable=False),
        sa.Column("asin", sa.String(length=32), nullable=True),
        sa.Column("product_name", sa.Text(), nullable=True),
        sa.Column("condition", sa.String(length=40), nullable=True),
        sa.Column("fulfillable_quantity", sa.Numeric(12, 3), nullable=False),
        sa.Column("warehouse_quantity", sa.Numeric(12, 3), nullable=False),
        sa.Column("unsellable_quantity", sa.Numeric(12, 3), nullable=False),
        sa.Column("reserved_quantity", sa.Numeric(12, 3), nullable=False),
        sa.Column("total_quantity", sa.Numeric(12, 3), nullable=False),
        sa.Column("inbound_working_quantity", sa.Numeric(12, 3), nullable=False),
        sa.Column("inbound_shipped_quantity", sa.Numeric(12, 3), nullable=False),
        sa.Column("inbound_receiving_quantity", sa.Numeric(12, 3), nullable=False),
        sa.Column("researching_quantity", sa.Numeric(12, 3), nullable=False),
        sa.Column("raw_row", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("captured_at", "sku", "fnsku", name="uq_fba_inventory_snapshot_sku"),
    )
    for column in ("captured_at", "marketplace", "sku", "fnsku", "asin"):
        op.create_index(op.f(f"ix_fba_inventory_snapshots_{column}"), "fba_inventory_snapshots", [column], unique=False)


def downgrade() -> None:
    for column in ("asin", "fnsku", "sku", "marketplace", "captured_at"):
        op.drop_index(op.f(f"ix_fba_inventory_snapshots_{column}"), table_name="fba_inventory_snapshots")
    op.drop_table("fba_inventory_snapshots")
