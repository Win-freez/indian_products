from typing import Annotated

from fastapi import APIRouter, Depends, status, Path
from sqlalchemy.ext.asyncio import AsyncSession

from src.cart.dao import CartDAO
from src.cart.dependencies import get_cart_info
from src.cart.models import Cart
from src.cart.schemas import CartItemChangeSchema, CartItemSchema, CartOutSchema
from src.database import get_db
from src.users.dependencies import get_user_using_token
from src.users.models import User

router = APIRouter(prefix="/cart", tags=["Корзина"])


@router.get("/", status_code=status.HTTP_200_OK)
async def get_cart(
        db: Annotated[AsyncSession, Depends(get_db)],
        user: Annotated[User, Depends(get_user_using_token)],
) -> CartOutSchema:
    cart = await CartDAO.get_cart(db=db, user=user)

    return CartOutSchema.model_validate(cart)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_item_to_cart(
        db: Annotated[AsyncSession, Depends(get_db)],
        user: Annotated[User, Depends(get_user_using_token)],
        cart: Annotated[Cart, Depends(get_cart_info)],
        item: CartItemChangeSchema,
) -> CartItemSchema:
    cart_item = await CartDAO.add_item_to_cart(db=db, user=user, cart=cart, item=item)
    return CartItemSchema.model_validate(cart_item)


@router.patch("/", status_code=status.HTTP_200_OK)
async def change_item_in_cart(
        db: Annotated[AsyncSession, Depends(get_db)],
        user: Annotated[User, Depends(get_user_using_token)],
        cart: Annotated[Cart, Depends(get_cart_info)],
        item: CartItemChangeSchema,
) -> CartItemSchema:
    cart_item = await CartDAO.change_item_in_cart(
        db=db, user=user, cart=cart, item=item
    )

    return CartItemSchema.model_validate(cart_item)


@router.delete("/{slug}", status_code=status.HTTP_204_NO_CONTENT)
async def del_item_in_cart(
        db: Annotated[AsyncSession, Depends(get_db)],
        user: Annotated[User, Depends(get_user_using_token)],
        cart: Annotated[Cart, Depends(get_cart_info)],
        slug: Annotated[str, Path()],
):
    await CartDAO.del_item_from_cart(db=db, slug=slug, user=user, cart=cart)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def clear_cart(
        db: Annotated[AsyncSession, Depends(get_db)],
        user: Annotated[User, Depends(get_user_using_token)],
        cart: Annotated[Cart, Depends(get_cart_info)],
):
    await CartDAO.clear_cart(db=db, user=user, cart=cart)

