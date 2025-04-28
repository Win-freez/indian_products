from decimal import Decimal
from decimal import Decimal
from typing import Optional

from sqlalchemy import Integer, String, Text, ForeignKey, Float, DECIMAL, Boolean, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    image_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    stock: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    rating: Mapped[float] = mapped_column(Float, nullable=True, default=0.0)
    category_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL"), nullable=True
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default=text("TRUE")
    )

    category: Mapped["Category"] = relationship(
        "Category", back_populates="products", passive_deletes=True
    )
