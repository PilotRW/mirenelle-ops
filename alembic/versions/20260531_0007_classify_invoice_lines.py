"""classify invoice lines

Revision ID: 20260531_0007
Revises: 20260531_0006
Create Date: 2026-05-31 18:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


revision: str = "20260531_0007"
down_revision: Union[str, None] = "20260531_0006"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("purchase_invoice_lines", sa.Column("line_type", sa.String(length=40), nullable=False, server_default="product"))
    op.add_column("purchase_invoice_lines", sa.Column("expense_category", sa.String(length=80), nullable=True))
    op.create_index(op.f("ix_purchase_invoice_lines_expense_category"), "purchase_invoice_lines", ["expense_category"], unique=False)
    op.create_index(op.f("ix_purchase_invoice_lines_line_type"), "purchase_invoice_lines", ["line_type"], unique=False)

    op.execute(
        """
        update purchase_invoice_lines
        set line_type = 'inbound_shipping',
            expense_category = 'inbound_shipping'
        where product_name ~* '(versand|shipping|delivery|freight|transport|porto|livraison|spedizione|env[ií]o|wysy[lł]ka|dostawa|bezorg|frakt)'
        """
    )
    op.execute(
        """
        update product_cost_imports pci
        set row_count = counts.row_count
        from (
            select import_id, count(*) as row_count
            from product_costs
            group by import_id
        ) counts
        where pci.id = counts.import_id
          and pci.source_filename ilike 'invoice_costs_%'
        """
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_purchase_invoice_lines_line_type"), table_name="purchase_invoice_lines")
    op.drop_index(op.f("ix_purchase_invoice_lines_expense_category"), table_name="purchase_invoice_lines")
    op.drop_column("purchase_invoice_lines", "expense_category")
    op.drop_column("purchase_invoice_lines", "line_type")
