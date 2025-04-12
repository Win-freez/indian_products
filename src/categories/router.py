from tkinter.font import names
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.categories.schemas import CategorySchema
from src.categories.models import Category
from src.database import get_db


router = APIRouter(prefix='/categories', tags=['category'])


@router.get('/')
async def get_all_categories():
    pass


@router.post('/')
async def create_category(db: Annotated[AsyncSession, Depends(get_db)], category: CategorySchema):
    new_category = Category(name=category.name)
    db.add(new_category)

    await db.commit()
    await db.refresh(new_category)

    return new_category


@router.put('/')
async def update_category():
    pass


@router.delete('/')
async def delete_category():
    pass

