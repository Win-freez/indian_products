import enum
from decimal import Decimal

from sqlalchemy import Integer, ForeignKey, DECIMAL, Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base


class OrderEnum(enum.Enum):
    pending = "pending"
    completed = "completed"
    cancelled = "cancelled"


class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    total_price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    status: Mapped[OrderEnum] = mapped_column(Enum(OrderEnum), default=OrderEnum.pending)

    user: Mapped['User'] = relationship('User', back_populates='orders')
    order_items: Mapped[list['OrderItem']] = relationship('OrderItem', back_populates='order')


class OrderItem(Base):
    __tablename__ = "orders_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id', ondelete='CASCADE'), nullable=False)
    product_slug: Mapped[str] = mapped_column(String(255), nullable=False)
    product_name_snapshot: Mapped[str] = mapped_column(String(255), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price_at_time: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)

    order: Mapped['Order'] = relationship('Order', back_populates='order_items')

