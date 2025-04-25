from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import Base
from src.users import User
from src.users.dependencies import check_is_admin


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
    async def delete(cls, db: AsyncSession, obj: model, user: None | User = None) -> None:
        if user:
            check_is_admin(user)
        await db.delete(obj)
        await db.commit()
