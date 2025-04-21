from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.base_dao import BaseDao
from src.categories.schemas import CategorySchema
from src.categories.models import Category
from src.dependecies.dependencies import check_unique_slug


class CategoryDAO(BaseDao):
    model = Category

    @classmethod
    async def create_category(cls, db: AsyncSession, new_category: CategorySchema) -> Category:
        slug = await check_unique_slug(name=new_category.name, model=cls.model, db=db)
        category = await cls.create(db=db, **new_category.model_dump(), slug=slug)

        return category

    @classmethod
    async def update_category(cls, db: AsyncSession, category_data: CategorySchema, category: Category) -> Category:
        data = category_data.model_dump(exclude_unset=True)

        if 'name' in data and data['name'] != category.name:
            data['slug'] = await check_unique_slug(db=db, model=cls.model, name=data['name'])

        updated_category = await cls.update(db=db, instance=category, **data)

        return updated_category
