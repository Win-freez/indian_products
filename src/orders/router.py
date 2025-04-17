from typing import Annotated

from fastapi import APIRouter, Depends, status, Path
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.orders.dao import OrderDAO
from src.orders.schemas import OrderSchema, OrderOutSchema

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
    order = await OrderDAO.create_order(db=db, new_order=new_order)

    return OrderOutSchema.model_validate(order)
