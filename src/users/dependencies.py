from datetime import datetime, UTC
from typing import Annotated

from fastapi import Request, HTTPException, status, Depends
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.database import get_db
from src.users.dao import UserDao


def get_token(request: Request):
    token = request.cookies.get('access_token')
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='There is no token in cookies')
    return token


async def get_current_user(db: Annotated[AsyncSession, Depends(get_db)],
                           token: Annotated[str, Depends(get_token)]):
    try:
        payload = jwt.decode(token, key=settings.SECRET_KEY, algorithms=settings.ALGORITHM)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid access token')

    expire = payload.get('exp')
    if not expire or int(expire) < datetime.now(UTC).timestamp():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Time access token is out')

    user_id = payload.get('sub')
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User ID not found')

    user = await UserDao.get_user_by_id(db=db, user_id=int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')

    return user
