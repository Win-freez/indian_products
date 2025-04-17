from datetime import datetime
from typing import AsyncGenerator, Optional

from sqlalchemy import DateTime, func, MetaData
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.config import settings

async_engine = create_async_engine(settings.base_url, echo=True, pool_size=5, max_overflow=10)

async_session = async_sessionmaker(
    async_engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=settings.naming_convention)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, onupdate=datetime.utcnow, default=None)

    def __repr__(self):
        cols = []
        columns_to_show = 3
        for idx, col in enumerate(self.__table__.columns.keys()):
            if idx < columns_to_show:
                col.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"
