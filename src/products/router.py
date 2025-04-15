from typing import Annotated

from fastapi import APIRouter, status, Depends, Response, HTTPException, Path
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.products.schemas import ProductSchema, ProductOutSchema, ProductFilters
from src.products.models import Product
from src.categories.models import Category
from src.database import get_db
from src.products.dependencies import product_by_slug
from src.products.dao import ProductDAO

router = APIRouter(prefix='/products', tags=['products'])


@router.get('/', status_code=status.HTTP_200_OK)
async def all_products(db: Annotated[AsyncSession, Depends(get_db)]) -> list[ProductOutSchema]:
    products = await ProductDAO.get_all_products(db)
    return [ProductOutSchema.model_validate(product) for product in products]


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_product(db: Annotated[AsyncSession, Depends(get_db)],
                         new_product: ProductSchema,
                         response: Response) -> ProductOutSchema:
    product = await ProductDAO.create_product(db, new_product)
    response.headers['Location'] = f"{router.prefix}/{product.slug}"

    return ProductOutSchema.model_validate(product)


@router.get('/{category_slug}', status_code=status.HTTP_200_OK)
async def product_by_category(db: Annotated[AsyncSession, Depends(get_db)],
                              category_slug: str) -> list[ProductOutSchema]:
    products = await ProductDAO.get_product_by_category(db=db, category_slug=category_slug)

    return [ProductOutSchema.model_validate(product) for product in products]


@router.get('/products/filter', status_code=status.HTTP_200_OK)
async def filter_products(db: Annotated[AsyncSession, Depends(get_db)],
                          product_filters: ProductFilters = Depends()) -> list[ProductOutSchema]:
    products = await ProductDAO.get_filtered_products(db=db, product_filters=product_filters)

    return [ProductOutSchema.model_validate(product) for product in products]


@router.put('/{product_slug}')
async def update_product(db: Annotated[AsyncSession, Depends(get_db)],
                         product_data: ProductSchema,
                         product: Annotated[Product, Depends(product_by_slug)],
                         ) -> ProductOutSchema:
    product = await ProductDAO.update_product(db=db, product_data=product_data, product=product)
    return ProductOutSchema.model_validate(product)


@router.delete('/{product_slug}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_products(db: Annotated[AsyncSession, Depends(get_db)],
                          product: Product = Depends(product_by_slug)) -> None:
    await ProductDAO.delete_product(db=db, product=product)
