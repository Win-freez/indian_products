from fastapi import HTTPException, status
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.models import User
from src.users.schemas import UserRegisterSchema
from src.users.auth import hash_password, validate_password


class UserDao:
    ADMIN_EMAIL = "maria@example.com"

    @classmethod
    async def get_user_by_email(
        cls,
        db: AsyncSession,
        user_email: EmailStr,
    ) -> User | None:
        stmt = select(User).where(User.email == user_email)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        return user

    @classmethod
    async def get_user_by_id(
        cls,
        db: AsyncSession,
        user_id: int,
    ) -> User | None:
        stmt = select(User).where(User.id == user_id)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        return user

    @classmethod
    async def create_user(
        cls,
        db: AsyncSession,
        user_data: UserRegisterSchema,
    ) -> User:
        existing_user = await cls.get_user_by_email(db=db, user_email=user_data.email)

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User with email: {user_data.email} already exists",
            )

        hashed_password = hash_password(user_data.password)

        user = User(
            **user_data.model_dump(exclude={"password"}),
            hashed_password=hashed_password,
        )
        db.add(user)

        await db.commit()
        await db.refresh(user)

        return user

    @classmethod
    async def validate_user(
        cls,
        db: AsyncSession,
        email: EmailStr,
        password: str,
    ) -> User:
        user = await cls.get_user_by_email(db=db, user_email=email)

        if not user or not validate_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Wrong email or password",
            )

        return user

    @classmethod
    async def set_admin(
        cls,
        db: AsyncSession,
        user: User,
        user_id: int,
    ) -> User:
        user_to_update = await cls.get_user_by_id(db=db, user_id=user_id)

        if not user_to_update:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        if user_to_update.email == cls.ADMIN_EMAIL:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You cannot change admin rights for the first administrator.",
            )

        user_to_update.is_admin = not user_to_update.is_admin

        await db.commit()
        await db.refresh(user_to_update)

        return user_to_update
