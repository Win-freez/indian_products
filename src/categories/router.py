from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from slugify import slugify

from src.categories.schemas import CategorySchema
from src.categories.models import Category
from src.database import get_db

router = APIRouter(prefix='/categories', tags=['category'])


@router.get('/', status_code=status.HTTP_200_OK)
async def get_all_categories(db: Annotated[AsyncSession, Depends(get_db)]) -> list[CategorySchema]:
    stmt = select(Category).order_by(Category.name)
    result = await db.execute(stmt)
    categories = result.scalars().all()

    return [CategorySchema.model_validate(category) for category in categories]


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_category(db: Annotated[AsyncSession, Depends(get_db)],
                          category: CategorySchema,
                          response: Response) -> CategorySchema:
    new_category = Category(name=category.name,
                            slug=slugify(category.name),
                            parent_id=category.parent_id)
    db.add(new_category)

    await db.commit()
    await db.refresh(new_category)

    response.headers['Location'] = f"/{router.prefix}/{new_category.slug}"

    return CategorySchema.model_validate(new_category)


@router.put('/{category_slug}', status_code=status.HTTP_204_NO_CONTENT)
async def update_category(db: Annotated[AsyncSession, Depends(get_db)],
                          category_slug: str,
                          updated_category: CategorySchema) -> None:
    stmt = select(Category).where(Category.slug == category_slug)
    result = await db.execute(stmt)
    category = result.scalar_one_or_none()

    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Category not found')

    stmt = (
        update(Category)
        .where(Category.slug == category_slug)
        .values(name=updated_category.name,
                slug=slugify(updated_category.name),
                parent_id=updated_category.parent_id)
    )
    result = await db.execute(stmt)
    await db.commit()

    return None


@router.delete('/{category_slug}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(db: Annotated[AsyncSession, Depends(get_db)],
                          category_slug: str) -> None:
    stmt = select(Category).where(Category.slug == category_slug)
    result = await db.execute(stmt)
    category = result.scalar_one_or_none()

    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Category not found')

    stmt = delete(Category).where(Category.slug == category_slug)
    await db.execute(stmt)
    await db.commit()

    return None