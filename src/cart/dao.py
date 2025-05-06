from fastapi import HTTPException, status
from sqlalchemy import select, and_, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.cart.models import Cart, CartItem
from src.cart.schemas import CartItemChangeSchema
from src.products.models import Product
from src.users.models import User


class CartDAO:
    @classmethod
    async def _check_cart_owner(cls, cart: Cart, user: User):
        """
        Проверяет, принадлежит ли корзина текущему пользователю.

        :param cart: Объект корзины.
        :param user: Текущий пользователь.
        :raises HTTPException: 403, если корзина принадлежит другому пользователю.
        """
        if cart.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Невозможно изменить корзину другого пользователя"
            )

    @classmethod
    async def _get_cart_item(cls, db: AsyncSession, cart_id: int, slug: str) -> CartItem | None:
        """
        Получает товар из корзины по cart_id и slug продукта.

        :param db: Сессия базы данных.
        :param cart_id: ID корзины.
        :param slug: slug продукта.
        :return: CartItem или None, если товар не найден.
        """
        stmt = select(CartItem).where(
            and_(CartItem.cart_id == cart_id, CartItem.product_slug == slug)
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @classmethod
    async def _get_product(cls, db: AsyncSession, slug: str) -> Product:
        """
        Получает продукт по slug.

        :param db: Сессия базы данных.
        :param slug: slug продукта.
        :return: Объект Product.
        :raises HTTPException: 404, если продукт не найден.
        """
        stmt = select(Product).where(Product.slug == slug)
        result = await db.execute(stmt)
        product = result.scalar_one_or_none()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Товар по slug '{slug}' не найден"
            )
        return product

    @classmethod
    async def get_cart(cls, db: AsyncSession, user: User) -> Cart:
        """
         Получает корзину пользователя. Если корзины нет — создаёт новую.

         :param db: Сессия базы данных.
         :param user: Текущий пользователь.
         :return: Объект Cart с подгруженными товарами.
         """
        stmt = (
            select(Cart)
            .options(selectinload(Cart.cart_items))
            .where(Cart.user_id == user.id)
        )
        result = await db.execute(stmt)
        cart = result.scalar_one_or_none()

        if not cart:
            cart = Cart(user_id=user.id)
            db.add(cart)
            await db.commit()
            await db.refresh(cart)

        return cart

    @classmethod
    async def add_item_to_cart(cls,
                               db: AsyncSession,
                               user: User,
                               cart: Cart,
                               item: CartItemChangeSchema) -> CartItem:
        """
        Добавляет товар в корзину или увеличивает его количество, если он уже есть.

        :param db: Сессия базы данных.
        :param user: Текущий пользователь.
        :param cart: Корзина пользователя.
        :param item: Данные о товаре (slug и количество).
        :return: Обновлённый или новый CartItem.
        """

        # Проверка на принадлежность корзины пользователю
        await cls._check_cart_owner(cart, user)

        # Загрузка товара
        product = await cls._get_product(db=db, slug=item.product_slug)

        # Проверка на наличие аналогичного товара в корзине
        existing_item = await cls._get_cart_item(db=db,
                                                 cart_id=cart.id,
                                                 slug=item.product_slug)

        total_quantity = item.quantity
        if existing_item:
            total_quantity += existing_item.quantity

        # Проверка, что общее количество не превышает остаток на складе
        if total_quantity > product.stock:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Товара в наличии {product.stock} шт. Вы пытаетесь заказать {total_quantity}"
            )

        if existing_item:
            existing_item.quantity += item.quantity
            await db.commit()
            await db.refresh(existing_item)

            return existing_item

        # Создание нового CartItem
        new_item = CartItem(cart_id=cart.id,
                            product_slug=item.product_slug,
                            product_name_snapshot=product.name,
                            quantity=item.quantity,
                            price_at_time=product.price
                            )
        db.add(new_item)
        await db.commit()
        await db.refresh(new_item)

        return new_item

    @classmethod
    async def change_item_in_cart(cls,
                                  db: AsyncSession,
                                  user: User,
                                  cart: Cart,
                                  item: CartItemChangeSchema) -> CartItem | dict[str, str]:
        """
        Изменяет количество товара в корзине. Если количество = 0 — удаляет товар.

        :param db: Сессия базы данных.
        :param user: Текущий пользователь.
        :param cart: Корзина пользователя.
        :param item: Данные о товаре (slug и новое количество).
        :return: Обновлённый CartItem или сообщение об удалении.
        """

        # Проверка на принадлежность корзины пользователю
        await cls._check_cart_owner(cart, user)

        # Проверка на наличие товара в корзине
        existing_item = await cls._get_cart_item(db=db,
                                                 cart_id=cart.id,
                                                 slug=item.product_slug)
        if not existing_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Товар '{item.product_slug}' не найден в корзине."
            )

        # Если количество = 0 — удаляем товар из корзины и возвращаем удаленную модель с количеством 0
        if item.quantity == 0:
            await db.delete(existing_item)
            await db.commit()

            existing_item.quantity = 0
            return existing_item

        # Получаем товар, чтобы проверить stock
        product = await cls._get_product(db=db, slug=item.product_slug)

        # Проверка: новое количество не больше чем есть в наличии
        if item.quantity > product.stock:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Товара в наличии {product.stock} шт. Вы пытаетесь установить {item.quantity}"
            )

        # Обновляем количество
        existing_item.quantity = item.quantity
        await db.commit()
        await db.refresh(existing_item)

        return existing_item

    @classmethod
    async def del_item_from_cart(cls,
                                 db: AsyncSession,
                                 slug: str,
                                 user: User,
                                 cart: Cart):
        """
        Удаляет товар из корзины по slug.

        :param db: Сессия базы данных.
        :param slug: slug продукта.
        :param user: Текущий пользователь.
        :param cart: Корзина пользователя.
        :return: Сообщение об удалении.
        """
        # Проверка на принадлежность корзины пользователю
        await cls._check_cart_owner(cart, user)

        # Проверка на наличие товара в корзине
        existing_item = await cls._get_cart_item(db=db,
                                                 cart_id=cart.id,
                                                 slug=slug)
        if not existing_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Такого товара в корзине не найдено"
            )

        await db.delete(existing_item)
        await db.commit()

        return {"detail": f"Товар с slug '{slug}' был удален из корзины."}

    @classmethod
    async def clear_cart(cls,
                         db: AsyncSession,
                         user: User,
                         cart: Cart) -> None:
        """
        Полностью очищает корзину пользователя (удаляет все товары).

        :param db: Сессия базы данных.
        :param user: Текущий пользователь.
        :param cart: Корзина пользователя.
        """
        # Проверка на принадлежность корзины пользователю
        await cls._check_cart_owner(cart, user)
        # Удаление всех товаров из корзины
        stmt = delete(CartItem).where(CartItem.cart_id == cart.id)
        await db.execute(stmt)
        await db.commit()
