from typing import Optional

from sqlalchemy import String, event, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from slugify import slugify

from src.database import Base


class Category(Base):
    __tablename__ = 'categories'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey('categories.id', ondelete='SET NULL'), nullable=True)
    
    products: Mapped[list["Product"]] = relationship('Product', back_populates='category')


@event.listens_for(Category, 'before_insert')
def generate_slug(mapper, connection, target):
    if not target.slug:
        target.slug = slugify(target.name)