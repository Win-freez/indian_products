from datetime import datetime, timezone
from typing import Annotated

from fastapi import HTTPException, status, Depends, Request
from jwt import PyJWTError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.users.auth import decode_jwt
from src.users.dao import UserDao
from src.users.models import User


def get_access_token(request: Request) -> str:
    token = request.cookies.get('access_token')
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token not found')
    return token


async def get_user_using_token(db: Annotated[AsyncSession, Depends(get_db)],
                               token: Annotated[str, Depends(get_access_token)]):
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


def check_user_is_admin(user: User = Depends(get_user_using_token)) -> User:
    if not user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not allowed. Only admin has access')
    return user
