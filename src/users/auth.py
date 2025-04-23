from datetime import datetime, timedelta, UTC

from fastapi import Request, HTTPException, status
from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.users.dao import UserDao

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(hours=1)
    to_encode.update({'exp': expire})
    auth_data = settings.auth_data
    encode_jwt = jwt.encode(to_encode, key=auth_data['secret_key'], algorithm=auth_data['algorithm'])
    return encode_jwt


async def authenticate_user(db: AsyncSession, email: EmailStr, password: str):
    user = await UserDao.get_user_by_email(db=db, user_email=email)
    if not user or verify_password(plain_password=password, hashed_password=user.hashed_password) is False:
        return None
    return user

