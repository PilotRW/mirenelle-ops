"""add bundle component recipes

Revision ID: 20260619_0017
Revises: 20260619_0016
Create Date: 2026-06-19 16:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


revision: str = "20260619_0017"
down_revision: Union[str, None] = "20260619_0016"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "bundle_components",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("bundle_sku", sa.String(length=160), nullable=False),
        sa.Column("bundle_name", sa.String(length=500), nullable=True),
        sa.Column("component_sku", sa.String(length=160), nullable=False),
        sa.Column("component_quantity", sa.Numeric(precision=12, scale=3), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "bundle_sku",
            "component_sku",
            name="uq_bundle_components_bundle_component",
        ),
    )
    op.create_index("ix_bundle_components_bundle_sku", "bundle_components", ["bundle_sku"])
    op.create_index("ix_bundle_components_component_sku", "bundle_components", ["component_sku"])


def downgrade() -> None:
    op.drop_table("bundle_components")
