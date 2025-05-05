from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy import select, update, case, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from src.dao.base_dao import BaseDao
from src.orders.models import Order, OrderItem
from src.orders.schemas import OrderCreateSchema, OrderEnum
from src.products.models import Product
from src.users.models import User


class OrderDAO(BaseDao):

    @classmethod
    async def get_all_order(cls, db: AsyncSession, user: User) -> list[Order]:
        if user.is_admin:
            stmt = select(Order)
        else:
            stmt = (
                select(Order)
                .where(Order.user_id == user.id)
            )
        result = await db.execute(stmt)
        orders = result.unique().scalars().all()

        return list(orders)

    @classmethod
    async def get_user_order_by_id(
            cls, db: AsyncSession,
            user: User,
            object_id: int
    ) -> Order:
        if user.is_admin:
            stmt = (select(Order)
                    .where(Order.id == object_id)
                    .options(selectinload(Order.order_items))
                    )
        else:
            stmt = (select(Order)
                    .where(and_(Order.id == object_id, Order.user_id == user.id))
                    .options(selectinload(Order.order_items))
                    )
        result = await db.execute(stmt)
        order = result.scalar_one_or_none()

        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Заказ с ID {object_id} не найден",
            )

        return order

    @classmethod
    async def create_order(
            cls, db: AsyncSession, user: User, new_order: OrderCreateSchema
    ) -> Order:

        order = Order(
            user_id=user.id, total_price=Decimal("0.00"), status=OrderEnum.pending
        )

        db.add(order)
        await db.flush()

        slugs = [item.product_slug for item in new_order.order_items]
        stmt = select(Product).where(Product.slug.in_(slugs))
        result = await db.execute(stmt)
        products = {product.slug: product for product in result.scalars().all()}

        missing_slugs = [
            item.product_slug
            for item in new_order.order_items
            if item.product_slug not in products
        ]
        if missing_slugs:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Товары с такими slugs не найдены: {', '.join(missing_slugs)}",
            )

        order_items = []
        total_price = 0

        for item in new_order.order_items:

            product = products[item.product_slug]

            if item.quantity > product.stock:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Недостаточно товара в остатках: {product.name}. Остаток {product.stock}",
                )

            product.stock -= item.quantity
            total_price += item.quantity * product.price

            order_item = OrderItem(
                order_id=order.id,
                product_slug=product.slug,
                product_name_snapshot=product.name,
                quantity=item.quantity,
                price_at_time=product.price,
            )

            order_items.append(order_item)

        order.total_price = total_price

        db.add_all(order_items)
        await db.commit()

        user_order = await cls.get_user_order_by_id(
            db=db, user=user, object_id=order.id
        )

        return user_order

    @classmethod
    async def cancel_order(cls, db: AsyncSession, user: User, object_id: int):
        order = await cls.get_user_order_by_id(db=db, user=user, object_id=object_id)

        if order.status in {OrderEnum.cancelled, OrderEnum.completed}:
            raise HTTPException(
                status_code=400, detail="Заказ уже отменён или завершён"
            )

        products_to_return = {}

        for item in order.order_items:
            products_to_return[item.product_slug] = item.quantity

        stmt = (
            update(Product)
            .where(Product.slug.in_(products_to_return.keys()))
            .values(
                stock=case(
                    *[
                        (Product.slug == slug, Product.stock + quantity)
                        for slug, quantity in products_to_return.items()
                    ]
                )
            )
        )

        result = await db.execute(stmt)

        if result.rowcount == 0:
            raise HTTPException(
                status_code=500, detail="Ошибка обновления количества товаров"
            )

        order.status = OrderEnum.cancelled
        await db.commit()
        await db.refresh(order)

        return order
