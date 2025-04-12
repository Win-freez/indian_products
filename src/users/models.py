from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String(128), nullable=False)

    orders: Mapped[list['Order']] = relationship('Order', back_populates='user', cascade='all, delete-orphan')


