from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.cart.models import Cart
from src.database import get_db
from src.users.dependencies import get_user_using_token
from src.users.models import User


async def get_cart_info(
        db: AsyncSession = Depends(get_db),
        user: User = Depends(get_user_using_token),
) -> Cart:
    stmt = select(Cart).where(Cart.user_id == user.id)
    result = await db.execute(stmt)
    cart = result.scalar_one_or_none()

    if cart is None:
        # Создание корзину, если ее нет
        cart = Cart(user_id=user.id)
        db.add(cart)
        await db.commit()
        await db.refresh(cart)

    return cart
