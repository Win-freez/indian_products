from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from src.dao.base_dao import BaseDao
from src.products.models import Product
from src.products.schemas import ProductSchema, ProductFilters, ProductUpdateSchema
from src.dependecies.dependencies import check_unique_slug
from src.categories.models import Category


class ProductDAO(BaseDao):
    model = Product

    @classmethod
    async def create_product(cls, db: AsyncSession, new_product: ProductSchema) -> Product:
        slug = await check_unique_slug(name=new_product.name, model=Product, db=db)

        product = Product(**new_product.model_dump(), slug=slug)
        db.add(product)

        await db.commit()
        await db.refresh(product)

        return product

    @classmethod
    async def get_product_by_category(cls, db: AsyncSession, category_slug: str) -> list[Product]:
        stmt = select(Category).where(Category.slug == category_slug)
        result = await db.execute(stmt)
        category = result.scalar_one_or_none()

        if category is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

        stmt = (
            select(Product)
            .where(Product.category_id == category.id)
        )
        result = await db.execute(stmt)
        products = result.scalars().all()

        return list(products)

    @classmethod
    async def get_filtered_products(cls, db: AsyncSession, product_filters: ProductFilters) -> list[Product]:
        stmt = select(Product).join(Category, Product.category_id == Category.id)

        if product_filters.name:
            stmt = stmt.where(Product.name.ilike(f'%{product_filters.name}%'))
        if product_filters.min_price:
            stmt = stmt.where(Product.price >= product_filters.min_price)
        if product_filters.max_price:
            stmt = stmt.where(Product.price <= product_filters.max_price)
        if product_filters.category_slug:
            stmt = stmt.where(Category.slug == product_filters.category_slug)
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
    async def update_product(cls, db: AsyncSession, product_data: ProductSchema | ProductUpdateSchema, product: Product) -> Product:

        product_data_dict = product_data.model_dump(exclude_unset=True)
        new_name = product_data_dict.get('name')

        if new_name and new_name != product.name:
            slug = await check_unique_slug(db=db, model=Product, name=new_name)
            setattr(product, 'slug', slug)

        for key, value in product_data_dict.items():
            setattr(product, key, value)

        await db.commit()
        await db.refresh(product)

        return product


