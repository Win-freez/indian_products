from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.database import get_db
from src.users.dependencies import get_user_using_token
from src.users.models import User
from src.cart.models import Cart

router = APIRouter(prefix='/cart', tags=['Корзина'])


@router.get('/', status_code=status.HTTP_200_OK)
async def get_cart(db: Annotated[AsyncSession, Depends(get_db)],
                   user: Annotated[User, Depends(get_user_using_token)]):
    stmt = (select(Cart)
            .where(Cart.user_id==user.id)
            .options(selectinload(Cart.cart_items))
            )
    result = await db.execute(stmt)
    cart = result.scalar_one_or_none()

    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    return cart

