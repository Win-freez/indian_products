from typing import Annotated

from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.database import get_db
from src.users.auth import get_password_hash, authenticate_user, create_access_token
from src.users.dao import UserDao
from src.users.models import User
from src.users.schemas import UserAuthSchema, UserRegisterSchema
from src.users.dependencies import get_current_user
router = APIRouter(prefix='/auth', tags=['authentication'])

@router.get('/users')
async def get_users(db: Annotated[AsyncSession, Depends(get_db)],
                    user: Annotated[User, Depends(get_current_user)]):
    if not user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Access denied')
    stmt = select(User)
    result = await db.execute(stmt)
    return result.scalars().all()

@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register_user(db: Annotated[AsyncSession, Depends(get_db)],
                        user_data: UserRegisterSchema):
    existing_user = await UserDao.get_user_by_email(db=db, user_email=user_data.email)

    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"User with email: {user_data.email} already exists")

    hashed_password = get_password_hash(user_data.password)

    user = User(**user_data.model_dump(exclude={'password'}), hashed_password=hashed_password)

    db.add(user)
    await db.commit()

    return {'message': 'Register success'}


@router.post('/login')
async def login_user(db: Annotated[AsyncSession, Depends(get_db)],
                     user_data: UserAuthSchema,
                     response: Response):
    user = await authenticate_user(db=db, email=user_data.email, password=user_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Wrong email or password')
    access_token = create_access_token({'sub': str(user.id)})
    response.set_cookie('access_token', access_token, httponly=True)
    return {'message': 'Login success'}
