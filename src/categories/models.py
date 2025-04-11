from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Category(Base):
    __tablename__ = 'categories'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    products: Mapped[list["Product"]] = relationship('Product', back_populates='category')