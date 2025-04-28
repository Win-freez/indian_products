from typing import Annotated

from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.ext.asyncio import AsyncSession

from src.categories.dao import CategoryDAO
from src.categories.models import Category
from src.categories.schemas import CategorySchema, CategoryOutSchema
from src.database import get_db
from src.dependecies.dependencies import get_instance_by_slug
from src.users.dependencies import check_user_is_admin
from src.users.models import User

router = APIRouter(prefix='/categories', tags=['category'])


@router.get('/', status_code=status.HTTP_200_OK)
async def get_all_categories(db: Annotated[AsyncSession, Depends(get_db)]) -> list[CategoryOutSchema]:
    categories = await CategoryDAO.get_all(db=db)
    return [CategoryOutSchema.model_validate(category) for category in categories]


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_category(db: Annotated[AsyncSession, Depends(get_db)],
                          user: Annotated[User, Depends(check_user_is_admin)],
                          new_category: CategorySchema,
                          response: Response) -> CategoryOutSchema:
    new_category = await CategoryDAO.create_category(db=db, new_category=new_category)

    response.headers['Location'] = f"/{router.prefix}/{new_category.slug}"

    return CategoryOutSchema.model_validate(new_category)


@router.put('/{slug}', status_code=status.HTTP_200_OK)
async def update_category(db: Annotated[AsyncSession, Depends(get_db)],
                          user: Annotated[User, Depends(check_user_is_admin)],
                          category: Annotated[Category, Depends(get_instance_by_slug(Category))],
                          category_data: CategorySchema) -> CategoryOutSchema:
    category = await CategoryDAO.update_category(db=db, category=category, category_data=category_data)
    return CategoryOutSchema.model_validate(category)


@router.delete('/{slug}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(db: Annotated[AsyncSession, Depends(get_db)],
                          user: Annotated[User, Depends(check_user_is_admin)],
                          category: Annotated[Category, Depends(get_instance_by_slug(Category))]) -> None:
    await CategoryDAO.delete(db=db, obj=category)
