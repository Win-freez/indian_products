from typing import Annotated

from slugify import slugify
from fastapi import HTTPException, status, Path, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.products.models import Product


async def product_by_slug(db: Annotated[AsyncSession, Depends(get_db)],
                          slug: Annotated[str, Path]) -> Product:
    stmt = select(Product).where(Product.slug == slug)

    result = await db.execute(stmt)
    product = result.scalar_one_or_none()

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with slug '{slug}' not found"
        )

    return product


async def check_unique_product_slug(name: str, db: Annotated[AsyncSession, Depends(get_db)]) -> str:
    slug = slugify(name)

    stmt = select(Product).where(Product.slug == slug)
    result = await db.execute(stmt)
    existing = result.scalar_one_or_none()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Product with slug '{slug}' already exists."
        )

    return slug
