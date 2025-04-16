from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.database import get_db
from src.orders.models import Order
from src.orders.schemas import OrderItemSchema, OrderSchema
from src.dependecies.dependencies import get_item_by_id

router = APIRouter(prefix='/orders', tags=['orders'])


@router.get('/')
async def get_orders(db: Annotated[AsyncSession, Depends(get_db)]) -> list[OrderSchema]:
    stmt = select(Order).order_by(Order.updated_at, Order.created_at)
    result = await db.execute(stmt)
    orders = result.scalars().all()

    return list(OrderSchema.model_validate(order) for order in orders)


@router.get('/{id}', status_code=status.HTTP_200_OK)
async def get_order(db: Annotated[AsyncSession, Depends(get_db)],
                    order: Annotated[Order, Depends(get_item_by_id(Order))]
                    ) -> OrderSchema:
    return OrderSchema.model_validate(order)
