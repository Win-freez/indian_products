from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision: str = 'c0bf47f23cd6'
down_revision: Union[str, None] = 'bb8fed6cee94'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# enum для статуса заказа
order_status_enum = postgresql.ENUM('pending', 'completed', 'cancelled', name='orderenum', create_type=False)

def upgrade():
    # временные таблицы
    op.create_table(
        'orders_temp',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('total_price', sa.DECIMAL(10, 2), nullable=False),
        sa.Column('status', order_status_enum, nullable=False, server_default='pending'),
    )

    op.create_table(
        'orders_items_temp',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('order_id', sa.Integer, nullable=False),
        sa.Column('product_slug', sa.String(length=255), nullable=False),
        sa.Column('product_name_snapshot', sa.String(length=255), nullable=False),
        sa.Column('quantity', sa.Integer, nullable=False),
        sa.Column('price_at_time', sa.DECIMAL(10, 2), nullable=False),
    )

    # перенос данных
    op.execute("""
        INSERT INTO orders_temp (id, user_id, total_price, status)
        SELECT id, user_id, total_price, status FROM orders
    """)

    op.execute("""
        INSERT INTO orders_items_temp (id, order_id, product_slug, product_name_snapshot, quantity, price_at_time)
        SELECT id, order_id, product_slug, product_name_snapshot, quantity, price_at_time FROM orders_items
    """)

    # удаление старых таблиц
    op.drop_table('orders_items')
    op.drop_table('orders')

    # переименование
    op.rename_table('orders_temp', 'orders')
    op.rename_table('orders_items_temp', 'orders_items')

    # восстановление foreign keys
    op.create_foreign_key('fk_order_user', 'orders', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('fk_item_order', 'orders_items', 'orders', ['order_id'], ['id'], ondelete='CASCADE')


def downgrade():
    # необязательно — можно реализовать по желанию
    raise NotImplementedError("Downgrade is not supported.")
