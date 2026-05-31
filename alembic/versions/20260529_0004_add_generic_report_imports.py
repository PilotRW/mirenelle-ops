"""add generic report imports

Revision ID: 20260529_0004
Revises: 20260529_0003
Create Date: 2026-05-29
"""

from typing import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


revision: str = "20260529_0004"
down_revision: str | None = "20260529_0003"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "generic_report_imports",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("report_type", sa.String(length=64), nullable=False),
        sa.Column("source_filename", sa.String(length=255), nullable=False),
        sa.Column("source_sha256", sa.String(length=64), nullable=True),
        sa.Column("row_count", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("source_sha256"),
    )
    op.create_index(op.f("ix_generic_report_imports_report_type"), "generic_report_imports", ["report_type"], unique=False)

    op.create_table(
        "generic_report_rows",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("import_id", sa.Integer(), nullable=False),
        sa.Column("row_number", sa.Integer(), nullable=False),
        sa.Column("raw_row", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["import_id"], ["generic_report_imports.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_generic_report_rows_import_id"), "generic_report_rows", ["import_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_generic_report_rows_import_id"), table_name="generic_report_rows")
    op.drop_table("generic_report_rows")
    op.drop_index(op.f("ix_generic_report_imports_report_type"), table_name="generic_report_imports")
    op.drop_table("generic_report_imports")

