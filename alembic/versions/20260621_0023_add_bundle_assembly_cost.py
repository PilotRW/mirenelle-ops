"""add bundle assembly cost

Revision ID: 20260621_0023
Revises: 20260621_0022
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


revision: str = "20260621_0023"
down_revision: Union[str, None] = "20260621_0022"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "bundle_assemblies",
        sa.Column(
            "assembly_provider",
            sa.String(length=32),
            server_default="unknown",
            nullable=False,
        ),
    )
    op.add_column(
        "bundle_assemblies",
        sa.Column(
            "unit_assembly_cost",
            sa.Numeric(12, 4),
            server_default="0",
            nullable=False,
        ),
    )
    op.add_column(
        "bundle_assemblies",
        sa.Column(
            "currency",
            sa.String(length=8),
            server_default="EUR",
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_column("bundle_assemblies", "currency")
    op.drop_column("bundle_assemblies", "unit_assembly_cost")
    op.drop_column("bundle_assemblies", "assembly_provider")
