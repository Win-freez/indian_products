from typing import Annotated

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.users.schemas import UserRegisterSchema
from src.users.auth import get_password_hash, verify_password
from sqlalchemy import select

from src.users.models import User

router = APIRouter(prefix='/auth', tags=['authentication'])


@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register_user(db: Annotated[AsyncSession, Depends(get_db)],
                        user_data: UserRegisterSchema):
    stmt = select(User).where(User.email == user_data.email)
    result = await db.execute(stmt)
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"User with email: {user_data.email} already exists")

    hashed_password = get_password_hash(user_data.password)

    user = User(**user_data.model_dump(exclude={'password'}), hashed_password=hashed_password)

    db.add(user)
    await db.commit()

    return {'message' : 'Success'}
