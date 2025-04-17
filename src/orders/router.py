from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Depends, status, Path, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.database import get_db
from src.dependecies.dependencies import get_instance_by_slug
from src.orders.dao import OrderDAO
from src.orders.models import Order, OrderItem, OrderEnum
from src.orders.schemas import OrderSchema, OrderOutSchema
from src.products.models import Product

router = APIRouter(prefix='/orders', tags=['orders'])


@router.get('/', status_code=status.HTTP_200_OK)
async def get_orders(db: Annotated[AsyncSession, Depends(get_db)]) -> list[OrderSchema]:
    orders = await OrderDAO.get_orders(db=db)

    return list(OrderSchema.model_validate(order) for order in orders)


@router.get('/{id}', status_code=status.HTTP_200_OK)
async def get_order(db: Annotated[AsyncSession, Depends(get_db)],
                    id: Annotated[int, Path(..., description='ID заказа')]
                    ) -> OrderSchema:
    order = await OrderDAO.get_order_by_id(db=db, id=id)

    return OrderSchema.model_validate(order)


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_order(db: Annotated[AsyncSession, Depends(get_db)],
                       new_order: OrderSchema):
    total_price = 0

    order = Order(
        user_id=new_order.user_id,
        total_price=Decimal('0.00'),
        status=OrderEnum.pending
    )

    db.add(order)
    await db.flush()

    order_items = []

    for item in new_order.order_items:
        product = await get_instance_by_slug(Product)(db=db, slug=item.product_slug)
        total_price += item.quantity * product.price

        if item.quantity > product.stock:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Недостаточно товара в остатках: {product.name}")

        order_item = OrderItem(
            order_id=order.id,
            product_slug=product.slug,
            product_name_snapshot=product.name,
            quantity=item.quantity,
            price_at_time=product.price
        )

        order_items.append(order_item)

    order.total_price = total_price

    db.add_all(order_items)
    await db.commit()

    stmt = select(Order).where(Order.id==order.id).options(joinedload(Order.order_items))
    result = await db.execute(stmt)
    order_to_validate = result.unique().scalar_one_or_none()

    return OrderOutSchema.model_validate(order_to_validate)
