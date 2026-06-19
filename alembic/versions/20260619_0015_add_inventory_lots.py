"""add FIFO inventory lots

Revision ID: 20260619_0015
Revises: 20260618_0014
Create Date: 2026-06-19 12:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


revision: str = "20260619_0015"
down_revision: Union[str, None] = "20260618_0014"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "inventory_lots",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("invoice_line_id", sa.Integer(), nullable=False),
        sa.Column("product_cost_id", sa.Integer(), nullable=False),
        sa.Column("purchase_date", sa.Date(), nullable=False),
        sa.Column("supplier_sku", sa.String(length=120), nullable=True),
        sa.Column("sku", sa.String(length=120), nullable=True),
        sa.Column("ean", sa.String(length=64), nullable=True),
        sa.Column("product_name", sa.Text(), nullable=False),
        sa.Column("quantity_received", sa.Numeric(precision=12, scale=3), nullable=False),
        sa.Column("unit_cost", sa.Numeric(precision=12, scale=4), nullable=False),
        sa.Column("currency", sa.String(length=8), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["invoice_line_id"], ["purchase_invoice_lines.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["product_cost_id"], ["product_costs.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("invoice_line_id", name="uq_inventory_lots_invoice_line"),
    )
    for column in ("invoice_line_id", "product_cost_id", "purchase_date", "supplier_sku", "sku", "ean"):
        op.create_index(f"ix_inventory_lots_{column}", "inventory_lots", [column])

    op.execute(
        """
        insert into inventory_lots (
            invoice_line_id,
            product_cost_id,
            purchase_date,
            supplier_sku,
            sku,
            ean,
            product_name,
            quantity_received,
            unit_cost,
            currency
        )
        select distinct on (pil.id)
            pil.id,
            pc.id,
            pc.effective_date,
            pil.supplier_sku,
            pil.sku,
            pil.ean,
            pil.product_name,
            pil.quantity,
            pc.purchase_cost,
            pc.currency
        from product_costs pc
        join purchase_invoice_lines pil
          on pil.invoice_id = (pc.raw_row->>'invoice_id')::integer
         and pil.line_type = 'product'
         and (
              pil.sku = pc.sku
           or pil.supplier_sku = pc.sku
           or pil.ean = pc.sku
           or pil.product_name = pc.product_name
         )
        where pc.raw_row->>'source' = 'purchase_invoice'
        order by pil.id, pc.id desc
        """
    )


def downgrade() -> None:
    op.drop_table("inventory_lots")
