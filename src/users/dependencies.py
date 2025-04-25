from datetime import datetime, timezone
from typing import Annotated

from fastapi import HTTPException, status, Depends, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import PyJWTError
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.users.auth import validate_password, decode_jwt
from src.users.dao import UserDao
from src.users.models import User

Oauth2_scheme = OAuth2PasswordBearer(tokenUrl=r'/auth/login')


async def validate_user(db: Annotated[AsyncSession, Depends(get_db)],
                        form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> User:
    user = await UserDao.get_user_by_email(db, user_email=form_data.username)
    if not user or validate_password(form_data.password, user.hashed_password) is False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Wrong email or password')
    return user


async def get_user_using_token(db: Annotated[AsyncSession, Depends(get_db)],
                               token: Annotated[str, Depends(Oauth2_scheme)]):
    try:
        payload = decode_jwt(token)
    except PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid access token')

    expire = payload.get('exp')
    if expire and int(expire) < datetime.now(timezone.utc).timestamp():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Time Access token is out')

    user_id = payload.get('sub')
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User ID not found in Access token')

    user = await UserDao.get_user_by_id(db, int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

    return user


def check_is_admin(user: User) -> User:
    if not user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not allowed. Only admin has access')
    return user
