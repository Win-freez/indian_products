from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.models import User


class UserDao:

    @classmethod
    async def get_user_by_email(cls, db: AsyncSession, user_email: EmailStr) -> User | None:
        stmt = select(User).where(User.email == user_email)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()

        return user

    @classmethod
    async def get_user_by_id(cls, db: AsyncSession, user_id: int) -> User | None:
        stmt = select(User).where(User.id == user_id)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()

        return user