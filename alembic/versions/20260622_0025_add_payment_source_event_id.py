"""add payment source event id

Revision ID: 20260622_0025
Revises: 20260621_0024
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


revision: str = "20260622_0025"
down_revision: Union[str, None] = "20260621_0024"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "amazon_payment_transactions",
        sa.Column("source_event_id", sa.String(length=255), nullable=True),
    )
    op.create_index(
        op.f("ix_amazon_payment_transactions_source_event_id"),
        "amazon_payment_transactions",
        ["source_event_id"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_amazon_payment_transactions_source_event_id"),
        table_name="amazon_payment_transactions",
    )
    op.drop_column("amazon_payment_transactions", "source_event_id")
