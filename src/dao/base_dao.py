from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class BaseDao:
    model = None

    @classmethod
    async def get_all(cls, db: AsyncSession) -> list[model]:
        stmt = select(cls.model).order_by(cls.model.id)
        result = await db.execute(stmt)
        return list(result.scalars().all())

    @classmethod
    async def delete(cls, db: AsyncSession, obj: model) -> None:
        await db.delete(obj)
        await db.commit()
