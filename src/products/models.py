from typing import Optional
from src.database import Base
from sqlalchemy import Integer, String, Text, ForeignKey, DateTime, Float, func, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship
from decimal import Decimal
from datetime import datetime


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    image_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    stock: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    rating: Mapped[float] = mapped_column(Float, nullable=True, default=0.0)
    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey('categories.id', ondelete='SET NULL'), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, server_default=func.now())

    category: Mapped['Category'] = relationship('Category', back_populates='products', passive_deletes=True)

    order_item: Mapped['OrderItem'] = relationship('OrderItem', back_populates='products')