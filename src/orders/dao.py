from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from src.orders.models import Order


class OrderDAO:

    @classmethod
    async def get_orders(cls, db: AsyncSession) -> list[Order]:
        stmt = select(Order).options(joinedload(Order.order_items))
        result = await db.execute(stmt)
        orders = result.unique().scalars().all()

        return list(orders)

    @classmethod
    async def get_order_by_id(cls, db: AsyncSession, id: int) -> Order:
        stmt = select(Order).where(Order.id==id).options(joinedload(Order.order_items))
        result = await db.execute(stmt)
        order = result.unique().scalar_one_or_none()

        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Заказ с ID {id} не найден')

        return order
