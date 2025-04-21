from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import Base


class BaseDao:
    model = None

    @classmethod
    async def create(cls, db: AsyncSession, **kwargs):
        instance = cls.model(**kwargs)
        db.add(instance)
        try:
            await db.commit()
            await db.refresh(instance)
        except SQLAlchemyError:
            await db.rollback()
            raise
        return instance

    @classmethod
    async def update(cls, db: AsyncSession, instance: Base, **kwargs):
        for key, value in kwargs.items():
            setattr(instance, key, value)
        try:
            await db.commit()
            await db.refresh(instance)
        except SQLAlchemyError:
            await db.rollback()
            raise
        return instance

    @classmethod
    async def get_all(cls, db: AsyncSession) -> list[model]:
        stmt = select(cls.model).order_by(cls.model.id)
        result = await db.execute(stmt)
        return list(result.scalars().all())

    @classmethod
    async def delete(cls, db: AsyncSession, obj: model) -> None:
        await db.delete(obj)
        await db.commit()
