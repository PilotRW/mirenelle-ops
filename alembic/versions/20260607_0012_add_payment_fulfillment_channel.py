"""add payment fulfillment channel

Revision ID: 20260607_0012
Revises: 20260605_0011
Create Date: 2026-06-07 10:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


revision: str = "20260607_0012"
down_revision: Union[str, None] = "20260605_0011"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "amazon_payment_transactions",
        sa.Column("fulfillment_channel", sa.String(length=16), nullable=False, server_default="UNKNOWN"),
    )
    op.create_index(
        op.f("ix_amazon_payment_transactions_fulfillment_channel"),
        "amazon_payment_transactions",
        ["fulfillment_channel"],
        unique=False,
    )
    op.execute(
        """
        update amazon_payment_transactions
        set fulfillment_channel = case
            when lower(coalesce(
                nullif(raw_row->>'Versand', ''),
                nullif(raw_row->>'fulfillment', ''),
                nullif(raw_row->>'gestión logística', ''),
                nullif(raw_row->>'gestión logistica', ''),
                nullif(raw_row->>'expédition', ''),
                nullif(raw_row->>'expedition', '')
            )) in (
                'amazon',
                'fba',
                'fulfillment by amazon',
                'versand durch amazon',
                'expédié par amazon',
                'expedie par amazon',
                'logística de amazon',
                'logistica de amazon',
                'logistica di amazon',
                'verzonden door amazon',
                'fraktas av amazon'
            ) then 'FBA'
            when lower(coalesce(
                nullif(raw_row->>'Versand', ''),
                nullif(raw_row->>'fulfillment', ''),
                nullif(raw_row->>'gestión logística', ''),
                nullif(raw_row->>'gestión logistica', ''),
                nullif(raw_row->>'expédition', ''),
                nullif(raw_row->>'expedition', '')
            )) in (
                'seller',
                'merchant',
                'fbm',
                'verkäufer',
                'verkaufer',
                'vendedor',
                'vendeur',
                'venditore',
                'sprzedawca',
                'verkoper',
                'säljare',
                'saljare'
            ) then 'FBM'
            else 'UNKNOWN'
        end
        """
    )
    op.alter_column("amazon_payment_transactions", "fulfillment_channel", server_default=None)


def downgrade() -> None:
    op.drop_index(op.f("ix_amazon_payment_transactions_fulfillment_channel"), table_name="amazon_payment_transactions")
    op.drop_column("amazon_payment_transactions", "fulfillment_channel")
