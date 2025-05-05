from decimal import Decimal

from sqlalchemy import Integer, ForeignKey, String, DECIMAL
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.database import Base


class Cart(Base):
    __tablename__ = 'carts'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)

    user: Mapped["User"] = relationship("User", back_populates="user_cart", uselist=False)
    cart_items: Mapped[list["CartItem"]] = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")


class CartItem(Base):
    __tablename__ = 'cart_items'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey("carts.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    product_slug: Mapped[str] = mapped_column(String(255), nullable=False)
    product_name_snapshot: Mapped[str] = mapped_column(String(255), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price_at_time: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)

    cart: Mapped["Cart"] = relationship("Cart", back_populates="cart_items")
