from typing import Annotated

from fastapi import APIRouter, status, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.users.auth import encode_jwt
from src.users.dao import UserDao
from src.users.dependencies import validate_user, get_user_using_token
from src.users.models import User
from src.users.schemas import UserRegisterSchema, UserOutSchema, TokenSchema

router = APIRouter(prefix='/auth', tags=['authentication'])


@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register_user(db: Annotated[AsyncSession, Depends(get_db)],
                        user_data: UserRegisterSchema) -> UserOutSchema:
    user = await UserDao.create_user(db, user_data)

    return UserOutSchema.model_validate(user)


@router.post('/login')
async def login_user(db: Annotated[AsyncSession, Depends(get_db)],
                     user: Annotated[User, Depends(validate_user)]) -> TokenSchema:
    payload = {'sub': str(user.id),
               'email': user.email}

    token = encode_jwt(payload)
    return TokenSchema(access_token=token)


http_bearer = HTTPBearer()


@router.get('/me')
async def get_user_info(user: Annotated[User, Depends(get_user_using_token)]) -> UserOutSchema:
    return UserOutSchema.model_validate(user)

