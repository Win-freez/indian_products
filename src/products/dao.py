from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from src.categories.models import Category
from src.dao.base_dao import BaseDao
from src.dependecies.dependencies import check_unique_slug
from src.products.models import Product
from src.products.schemas import ProductSchema, ProductFilters, ProductUpdateSchema
from src.users.models import User


class ProductDAO(BaseDao):
    model = Product

    @classmethod
    async def get_all(cls, db: AsyncSession) -> list[Product]:
        """
        Получить все товары с подгрузкой категории.
        Возвращает список отсортированных по имени товаров.
        """
        stmt = (
            select(Product).options(joinedload(Product.category)).order_by(Product.name)
        )
        result = await db.execute(stmt)
        products = result.scalars().all()
        return list(products)

    @classmethod
    async def create_product(
        cls,
        db: AsyncSession,
        new_product: ProductSchema
    ) -> Product:
        """
        Создать новый товар. Доступно только администратору.
        Генерирует уникальный slug и сохраняет товар в базе.
        """
        slug = await check_unique_slug(name=new_product.name, model=cls.model, db=db)
        product = await cls.create(db=db, **new_product.model_dump(), slug=slug)
        return product

    @classmethod
    async def get_product_by_category(
        cls, db: AsyncSession, category_slug: str
    ) -> list[Product]:
        """
        Получить товары по slug категории. Если категория не найдена — ошибка 404.
        """
        stmt = select(Category).where(Category.slug == category_slug)
        result = await db.execute(stmt)
        category = result.scalar_one_or_none()

        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
            )

        stmt = (
            select(Product)
            .options(joinedload(Product.category))
            .where(Product.category_id == category.id)
        )
        result = await db.execute(stmt)
        products = result.scalars().all()

        return list(products)

    @classmethod
    async def get_filtered_products(
        cls, db: AsyncSession, product_filters: ProductFilters
    ) -> list[Product]:
        """
        Получить отфильтрованные товары по нескольким полям:
        имя, диапазон цен, категория, наличие, активность и рейтинг.
        """
        stmt = select(Product).options(joinedload(Product.category))

        if product_filters.name:
            stmt = stmt.where(Product.name.ilike(f"%{product_filters.name}%"))
        if product_filters.min_price:
            stmt = stmt.where(Product.price >= product_filters.min_price)
        if product_filters.max_price:
            stmt = stmt.where(Product.price <= product_filters.max_price)
        if product_filters.category_slug:
            stmt = stmt.where(Product.category.slug == product_filters.category_slug)
        if product_filters.in_stock is not None:
            stmt = stmt.where(Product.stock > 0)
        if product_filters.is_active is not None:
            stmt = stmt.where(Product.is_active == product_filters.is_active)
        if product_filters.min_rating:
            stmt = stmt.where(Product.rating >= product_filters.min_rating)

        result = await db.execute(stmt)
        products = result.scalars().all()

        return list(products)

    @classmethod
    async def update_product(
        cls,
        db: AsyncSession,
        product_data: ProductSchema | ProductUpdateSchema,
        product: Product,
    ) -> Product:
        """
        Обновить товар. Только для администратора.
        Обновляет slug при изменении имени и сохраняет изменения в БД.
        """
        data = product_data.model_dump(exclude_unset=True)

        if "name" in data and data["name"] != product.name:
            data["slug"] = await check_unique_slug(
                db=db, model=cls.model, name=data["name"]
            )

        updated_product = await cls.update(db=db, instance=product, **data)

        return updated_product
