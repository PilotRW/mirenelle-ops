"""add fx rates

Revision ID: 20260529_0003
Revises: 20260529_0002
Create Date: 2026-05-29
"""

from typing import Sequence

import sqlalchemy as sa
from alembic import op


revision: str = "20260529_0003"
down_revision: str | None = "20260529_0002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "fx_rates",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("currency", sa.String(length=8), nullable=False),
        sa.Column("rate_to_eur", sa.Numeric(precision=18, scale=8), nullable=False),
        sa.Column("effective_date", sa.Date(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("currency", "effective_date", name="uq_fx_rates_currency_effective_date"),
    )
    op.create_index(op.f("ix_fx_rates_currency"), "fx_rates", ["currency"], unique=False)
    op.create_index(op.f("ix_fx_rates_effective_date"), "fx_rates", ["effective_date"], unique=False)

    op.bulk_insert(
        sa.table(
            "fx_rates",
            sa.column("currency", sa.String),
            sa.column("rate_to_eur", sa.Numeric),
            sa.column("effective_date", sa.Date),
        ),
        [
            {"currency": "EUR", "rate_to_eur": 1.0, "effective_date": "2026-01-01"},
            {"currency": "SEK", "rate_to_eur": 0.087, "effective_date": "2026-01-01"},
            {"currency": "GBP", "rate_to_eur": 1.17, "effective_date": "2026-01-01"},
            {"currency": "PLN", "rate_to_eur": 0.235, "effective_date": "2026-01-01"},
        ],
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_fx_rates_effective_date"), table_name="fx_rates")
    op.drop_index(op.f("ix_fx_rates_currency"), table_name="fx_rates")
    op.drop_table("fx_rates")

