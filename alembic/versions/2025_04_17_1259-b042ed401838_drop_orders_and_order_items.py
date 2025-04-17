"""Drop orders and order_items

Revision ID: b042ed401838
Revises: c0bf47f23cd6
Create Date: 2025-04-17 12:59:47.695652

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b042ed401838'
down_revision: Union[str, None] = 'c0bf47f23cd6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_table('orders_items')
    op.drop_table('orders')
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
