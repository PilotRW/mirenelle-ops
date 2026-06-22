"""add product prep costs

Revision ID: 20260622_0026
Revises: 20260622_0025
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


revision: str = "20260622_0026"
down_revision: Union[str, None] = "20260622_0025"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "product_prep_costs",
        sa.Column("sku", sa.String(length=120), nullable=False),
        sa.Column("fba_prep_per_unit", sa.Numeric(12, 4), nullable=False, server_default="0"),
        sa.Column("fbm_prep_per_unit", sa.Numeric(12, 4), nullable=False, server_default="0"),
        sa.Column("currency", sa.String(length=8), nullable=False, server_default="EUR"),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("sku"),
    )


def downgrade() -> None:
    op.drop_table("product_prep_costs")
