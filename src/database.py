from datetime import datetime
from sqlalchemy import DateTime, func
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from config import settings


async_engine = create_async_engine(settings.base_url, echo=True, pool_size=5, max_overflow=10)

async_session = async_sessionmaker(async_engine)


class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, onupdate=datetime.utcnow, default=datetime.utcnow)
