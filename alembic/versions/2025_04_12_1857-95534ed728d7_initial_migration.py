"""Initial migration

Revision ID: 95534ed728d7
Revises: 
Create Date: 2025-04-12 18:57:25.297942

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '95534ed728d7'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('slug', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_categories')),
    sa.UniqueConstraint('name', name=op.f('uq_categories_name'))
    )
    op.create_index(op.f('ix_categories_slug'), 'categories', ['slug'], unique=True)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('hashed_password', sa.String(length=128), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_users')),
    sa.UniqueConstraint('email', name=op.f('uq_users_email')),
    sa.UniqueConstraint('username', name=op.f('uq_users_username'))
    )
    op.create_table('orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('total_price', sa.DECIMAL(precision=10, scale=2), nullable=False),
    sa.Column('status', sa.Enum('pending', 'completed', 'cancelled', name='orderenum'), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_orders_user_id_users'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_orders'))
    )
    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('slug', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('price', sa.DECIMAL(precision=10, scale=2), nullable=False),
    sa.Column('image_url', sa.String(length=255), nullable=True),
    sa.Column('stock', sa.Integer(), nullable=False),
    sa.Column('rating', sa.Float(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('is_active', sa.Boolean(), server_default=sa.text('TRUE'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], name=op.f('fk_products_category_id_categories'), ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_products'))
    )
    op.create_index(op.f('ix_products_slug'), 'products', ['slug'], unique=True)
    op.create_table('orders_items',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('price_at_time', sa.DECIMAL(precision=10, scale=2), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], name=op.f('fk_orders_items_order_id_orders'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], name=op.f('fk_orders_items_product_id_products'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_orders_items'))
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('orders_items')
    op.drop_index(op.f('ix_products_slug'), table_name='products')
    op.drop_table('products')
    op.drop_table('orders')
    op.drop_table('users')
    op.drop_index(op.f('ix_categories_slug'), table_name='categories')
    op.drop_table('categories')

