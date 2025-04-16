from typing import Annotated, Type

from slugify import slugify
from fastapi import HTTPException, status, Path, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import Base

from src.database import get_db
from src.products.models import Product


def get_instance_by_slug(model: Type[Base]):
    async def dependency(
            slug: str = Path(..., description="Slug объекта"),
            db: AsyncSession = Depends(get_db)
    ):
        stmt = select(model).where(model.slug == slug)
        result = await db.execute(stmt)
        instance = result.scalar_one_or_none()

        if instance is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{model.__name__} with slug '{slug}' not found"
            )
        return instance

    return dependency


async def check_unique_slug(
        name: str,
        model: Type[Base],
        db: AsyncSession
) -> str:
    slug = slugify(name)

    stmt = select(model).where(model.slug == slug)
    result = await db.execute(stmt)
    existing = result.scalar_one_or_none()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{model.__name__} with slug '{slug}' already exists."
        )

    return slug
