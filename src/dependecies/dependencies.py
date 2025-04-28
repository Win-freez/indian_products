from typing import Type

from fastapi import HTTPException, status, Path, Depends
from slugify import slugify
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import Base
from src.database import get_db


def get_instance_by_slug(model: Type[Base]):
    async def dependency(
        slug: str = Path(..., description="Slug объекта"),
        db: AsyncSession = Depends(get_db),
    ):
        stmt = select(model).where(model.slug == slug)
        result = await db.execute(stmt)
        instance = result.scalar_one_or_none()

        if instance is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{model.__name__} with slug '{slug}' not found",
            )
        return instance

    return dependency


async def check_unique_slug(name: str, model: Type[Base], db: AsyncSession) -> str:
    slug = slugify(name)

    stmt = select(model).where(model.slug == slug)
    result = await db.execute(stmt)
    existing = result.scalar_one_or_none()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{model.__name__} with slug '{slug}' already exists.",
        )

    return slug


def get_item_by_id(model: Type[Base]):
    async def dependency(
        object_id: int = Path(..., description="ID объекта"),
        db: AsyncSession = Depends(get_db),
    ) -> Base:
        stmt = select(model).where(model.id == object_id)
        result = await db.execute(stmt)

        item = result.scalar_one_or_none()

        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{model.__name__} с ID {object_id} не найден",
            )

        return item

    return dependency
