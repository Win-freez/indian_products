from typing import Annotated

from fastapi import APIRouter, Depends, status, Path
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.orders.dao import OrderDAO
from src.orders.schemas import OrderCreateSchema, OrderOutSchema

router = APIRouter(prefix='/orders', tags=['orders'])


@router.get('/', status_code=status.HTTP_200_OK)
async def get_orders(db: Annotated[AsyncSession, Depends(get_db)]) -> list[OrderOutSchema]:
    orders = await OrderDAO.get_all(db=db)

    return list(OrderOutSchema.model_validate(order) for order in orders)


@router.get('/{object_id}', status_code=status.HTTP_200_OK)
async def get_order(db: Annotated[AsyncSession, Depends(get_db)],
                    object_id: Annotated[int, Path(..., description='ID заказа')]
                    ) -> OrderOutSchema:
    order = await OrderDAO.get_order_by_id(db=db, object_id=object_id)

    return OrderOutSchema.model_validate(order)


@router.post('/{object_id}', status_code=status.HTTP_201_CREATED)
async def create_order(db: Annotated[AsyncSession, Depends(get_db)],
                       new_order: OrderCreateSchema) -> OrderOutSchema:
    order = await OrderDAO.create_order(db=db, new_order=new_order)

    return OrderOutSchema.model_validate(order)


@router.post('/{object_id}/cancel', status_code=status.HTTP_200_OK)
async def cancel_order(db: Annotated[AsyncSession, Depends(get_db)],
                       object_id: Annotated[int, Path(..., ge=0, description='ID заказа')]
                       ) -> OrderOutSchema:
    order = await OrderDAO.cancel_order(db=db, object_id=object_id)
    return OrderOutSchema.model_validate(order)


@router.delete('/{object_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(db: Annotated[AsyncSession, Depends(get_db)],
                       object_id: Annotated[int, Path(..., ge=0, description='ID заказа')]
                       ) -> None:
    order = await OrderDAO.get_order_by_id(db=db, object_id=object_id)
    await OrderDAO.delete(db=db, obj=order)
