from typing import Annotated

from fastapi import APIRouter, status, Depends, Response, HTTPException
from sqlalchemy import select
from slugify import slugify
from sqlalchemy.ext.asyncio import AsyncSession

from src.products.schemas import ProductSchema, ProductOutSchema
from src.products.models import Product
from src.categories.models import Category
from src.database import get_db

router = APIRouter(prefix='/products', tags=['products'])


@router.get('/', status_code=status.HTTP_200_OK)
async def all_products(db: Annotated[AsyncSession, Depends(get_db)]) -> list[ProductSchema]:
    stmt = select(Product)
    result = await db.execute(stmt)
    products = result.scalars().all()

    return [ProductSchema.model_validate(product) for product in products]


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_product(db: Annotated[AsyncSession, Depends(get_db)],
                         new_product: ProductSchema, response: Response) -> ProductOutSchema:
    product = Product(**new_product.model_dump(), slug=slugify(new_product.name))
    db.add(product)

    await db.commit()
    await db.refresh(product)

    response.headers['Location'] = f"{router.prefix}/{product.slug}"

    return ProductOutSchema.model_validate(product)


@router.get('/{category_slug}', status_code=status.HTTP_200_OK)
async def product_by_category(db: Annotated[AsyncSession, Depends(get_db)],
                              category_slug: str) -> list[ProductOutSchema]:
    stmt = select(Category).where(Category.slug == category_slug)
    result = await db.execute(stmt)
    category = result.scalar_one_or_none()

    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    stmt = select(Product).join(Product.category_id == Category.id).where(Product.category_id==category.id)
    result = await db.execute(stmt)

    return [ProductOutSchema.model_validate(product) for product in result.scalars().all()]

@router.get('/detail/{product_slug}')
async def product_detail(product_slug: str):
    pass


@router.put('/')
async def update_product():
    pass


@router.delete('/')
async def delete_products():
    pass
