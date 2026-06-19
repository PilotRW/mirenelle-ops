"""allow manual opening inventory lots

Revision ID: 20260619_0016
Revises: 20260619_0015
Create Date: 2026-06-19 14:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


revision: str = "20260619_0016"
down_revision: Union[str, None] = "20260619_0015"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("inventory_lots", "invoice_line_id", existing_type=sa.Integer(), nullable=True)
    op.alter_column("inventory_lots", "product_cost_id", existing_type=sa.Integer(), nullable=True)
    op.add_column(
        "inventory_lots",
        sa.Column("source", sa.String(length=40), server_default="purchase_invoice", nullable=False),
    )
    op.add_column("inventory_lots", sa.Column("notes", sa.Text(), nullable=True))
    op.create_index("ix_inventory_lots_source", "inventory_lots", ["source"])


def downgrade() -> None:
    op.drop_index("ix_inventory_lots_source", table_name="inventory_lots")
    op.drop_column("inventory_lots", "notes")
    op.drop_column("inventory_lots", "source")
    op.alter_column("inventory_lots", "product_cost_id", existing_type=sa.Integer(), nullable=False)
    op.alter_column("inventory_lots", "invoice_line_id", existing_type=sa.Integer(), nullable=False)
