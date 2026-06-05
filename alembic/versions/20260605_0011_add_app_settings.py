"""add app settings

Revision ID: 20260605_0011
Revises: 20260604_0010
Create Date: 2026-06-05 21:40:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


revision: str = "20260605_0011"
down_revision: Union[str, None] = "20260604_0010"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "app_settings",
        sa.Column("key", sa.String(length=120), nullable=False),
        sa.Column("value", sa.Text(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("key"),
    )
    op.execute(
        "insert into app_settings (key, value) values "
        "('landed_cost_allocation_method', 'by_quantity') "
        "on conflict (key) do nothing"
    )


def downgrade() -> None:
    op.drop_table("app_settings")
