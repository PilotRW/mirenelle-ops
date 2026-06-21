"""add bundle assemblies

Revision ID: 20260621_0022
Revises: 20260621_0021
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


revision: str = "20260621_0022"
down_revision: Union[str, None] = "20260621_0021"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "bundle_assemblies",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("bundle_sku", sa.String(length=160), nullable=False),
        sa.Column("assembly_date", sa.Date(), nullable=False),
        sa.Column("quantity", sa.Numeric(12, 3), nullable=False),
        sa.Column("component_snapshot", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_bundle_assemblies_bundle_sku"),
        "bundle_assemblies",
        ["bundle_sku"],
        unique=False,
    )
    op.create_index(
        op.f("ix_bundle_assemblies_assembly_date"),
        "bundle_assemblies",
        ["assembly_date"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_bundle_assemblies_assembly_date"), table_name="bundle_assemblies")
    op.drop_index(op.f("ix_bundle_assemblies_bundle_sku"), table_name="bundle_assemblies")
    op.drop_table("bundle_assemblies")
