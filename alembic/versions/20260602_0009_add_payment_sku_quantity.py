"""add payment sku and quantity

Revision ID: 20260602_0009
Revises: 20260601_0008
Create Date: 2026-06-02 10:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


revision: str = "20260602_0009"
down_revision: Union[str, None] = "20260601_0008"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("amazon_payment_transactions", sa.Column("sku", sa.String(length=160), nullable=True))
    op.add_column("amazon_payment_transactions", sa.Column("quantity", sa.Numeric(12, 3), nullable=True))
    op.create_index(op.f("ix_amazon_payment_transactions_sku"), "amazon_payment_transactions", ["sku"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_amazon_payment_transactions_sku"), table_name="amazon_payment_transactions")
    op.drop_column("amazon_payment_transactions", "quantity")
    op.drop_column("amazon_payment_transactions", "sku")
