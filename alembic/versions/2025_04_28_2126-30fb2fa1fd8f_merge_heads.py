"""Merge heads

Revision ID: 30fb2fa1fd8f
Revises: aa1873044221, 338ec4915ced
Create Date: 2025-04-28 21:26:52.864698

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '30fb2fa1fd8f'
down_revision: Union[str, None] = ('aa1873044221', '338ec4915ced')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
