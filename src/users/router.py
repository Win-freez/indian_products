from typing import Annotated

from fastapi import APIRouter, status, Depends, Response, Form, Path
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.users.auth import encode_jwt
from src.users.dao import UserDao
from src.users.dependencies import get_user_using_token, check_user_is_admin
from src.users.models import User
from src.users.schemas import UserRegisterSchema, UserOutSchema

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    db: Annotated[AsyncSession, Depends(get_db)], user_data: UserRegisterSchema
) -> dict:
    user = await UserDao.create_user(db, user_data)

    return {
        "message": "Вы успешно зарегистрированы!",
        "user": UserOutSchema.model_validate(user),
    }


@router.post("/login")
async def login_user(
    db: Annotated[AsyncSession, Depends(get_db)],
    email: Annotated[EmailStr, Form()],
    password: Annotated[str, Form()],
    response: Response,
) -> dict:
    user = await UserDao.validate_user(db=db, email=email, password=password)

    payload = {"sub": str(user.id), "email": user.email}

    token = encode_jwt(payload)
    response.set_cookie(
        key="access_token", value=token, httponly=True, secure=True, samesite="lax"
    )

    return {"ok": True, "message": "Авторизация успешна!"}


@router.post("/logout")
async def logout_user(
    user: Annotated[User, Depends(get_user_using_token)], response: Response
) -> dict:
    response.delete_cookie("access_token", httponly=True, secure=True, samesite="lax")
    return {"message": f"User successfully logout"}


@router.get("/me")
async def get_user_info(
    user: Annotated[User, Depends(get_user_using_token)],
) -> UserOutSchema:
    return UserOutSchema.model_validate(user)


@router.post("/set-admin/{user_id}")
async def set_admin(
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(check_user_is_admin)],
    user_id: int = Path(gt=0),
) -> dict:
    user_to_update = await UserDao.set_admin(db=db, user=user, user_id=user_id)

    return {
        "message": f"User {user_to_update.email} is now {'an admin' if user_to_update.is_admin else 'not an admin'}",
        "user": UserOutSchema.model_validate(user_to_update),
    }
