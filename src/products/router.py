from typing import Annotated
import asyncio

from fastapi import APIRouter, status, Depends, Body, Path
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.database import get_db
from src.dependecies.dependencies import get_instance_by_slug
from src.products.cache import SlugKeyBuilder
from src.products.dao import ProductDAO
from src.products.models import Product
from src.products.schemas import (
    ProductSchema,
    ProductOutSchema,
    ProductFilters,
    ProductUpdateSchema,
)
from src.users.dependencies import check_user_is_admin
from src.users.models import User

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", status_code=status.HTTP_200_OK)
@cache(expire=60 * 30, namespace='products')
async def get_all_products(
        db: Annotated[AsyncSession, Depends(get_db)],
) -> list[ProductOutSchema]:
    products = await ProductDAO.get_all(db)
    return [ProductOutSchema.model_validate(product) for product in products]


@router.get("/{slug}", status_code=status.HTTP_200_OK)
@cache(expire=60 * 15, namespace=f'product', key_builder=SlugKeyBuilder())
async def get_product(
        db: Annotated[AsyncSession, Depends(get_db)],
        product: Annotated[Product, Depends(get_instance_by_slug(model=Product,
                                                                 load_strategy=joinedload,
                                                                 relationship='category'))],
) -> ProductOutSchema:
    return ProductOutSchema.model_validate(product)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_product(
        db: Annotated[AsyncSession, Depends(get_db)],
        user: Annotated[User, Depends(check_user_is_admin)],
        new_product: ProductSchema,
) -> ProductOutSchema:
    product = await ProductDAO.create_product(db=db, new_product=new_product)

    await FastAPICache.clear(namespace="products", key=f"product:{product.slug}")

    return ProductOutSchema.model_validate(product)


@router.get("/categories/{slug}", status_code=status.HTTP_200_OK)
@cache(expire=60 * 60, namespace='category_products')
async def products_by_category(
        db: Annotated[AsyncSession, Depends(get_db)],
        slug: Annotated[str, Path(...,
                                  min_length=3,
                                  max_length=255,
                                  description='Категория товара')],
) -> list[ProductOutSchema]:
    products = await ProductDAO.get_products_by_category(db=db, category_slug=slug)

    return [ProductOutSchema.model_validate(product) for product in products]


@router.get("/filter", status_code=status.HTTP_200_OK)
async def filter_products(
        db: Annotated[AsyncSession, Depends(get_db)],
        product_filters: ProductFilters = Depends(),
) -> list[ProductOutSchema]:
    products = await ProductDAO.get_filtered_products(
        db=db, product_filters=product_filters
    )

    return [ProductOutSchema.model_validate(product) for product in products]


@router.put("/{slug}")
async def update_product(
        db: Annotated[AsyncSession, Depends(get_db)],
        user: Annotated[User, Depends(check_user_is_admin)],
        product_data: Annotated[ProductSchema, Body()],
        product: Annotated[Product, Depends(get_instance_by_slug(Product))],
) -> ProductOutSchema:
    product = await ProductDAO.update_product(
        db=db, product_data=product_data, product=product
    )
    await FastAPICache.clear(namespace='product', key=f'product:{product.slug}')

    return ProductOutSchema.model_validate(product)


@router.patch("/{slug}")
async def update_product_partition(
        db: Annotated[AsyncSession, Depends(get_db)],
        user: Annotated[User, Depends(check_user_is_admin)],
        product_data: ProductUpdateSchema,
        product: Annotated[Product, Depends(get_instance_by_slug(Product))],
) -> ProductOutSchema:
    product = await ProductDAO.update_product(
        db=db, product_data=product_data, product=product
    )
    await FastAPICache.clear(namespace="product", key=f"product:{product.slug}")
    return ProductOutSchema.model_validate(product)


@router.delete("/{slug}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
        db: Annotated[AsyncSession, Depends(get_db)],
        user: Annotated[User, Depends(check_user_is_admin)],
        product: Product = Depends(get_instance_by_slug(Product)),
) -> None:
    await ProductDAO.delete(db=db, obj=product)
    await FastAPICache.clear(namespace='products')
    await FastAPICache.clear(namespace="product", key=f"product:{product.slug}")
