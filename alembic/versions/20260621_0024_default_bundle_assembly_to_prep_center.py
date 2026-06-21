"""default bundle assembly provider to prep center

Revision ID: 20260621_0024
Revises: 20260621_0023
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


revision: str = "20260621_0024"
down_revision: Union[str, None] = "20260621_0023"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "bundle_assemblies",
        "assembly_provider",
        existing_type=sa.String(length=32),
        server_default="prep_center",
        existing_nullable=False,
    )


def downgrade() -> None:
    op.alter_column(
        "bundle_assemblies",
        "assembly_provider",
        existing_type=sa.String(length=32),
        server_default="unknown",
        existing_nullable=False,
    )
