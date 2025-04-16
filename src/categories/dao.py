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
        slug = await check_unique_slug(name=new_category.name, model=Category, db=db)

        category = Category(**new_category.model_dump(), slug=slug)
        db.add(category)

        await db.commit()
        await db.refresh(category)

        return category

    @classmethod
    async def update_category(cls, db: AsyncSession, category_data: CategorySchema, category: Category) -> Category:

        category_data_dict = category_data.model_dump(exclude_unset=True)
        new_name = category_data_dict.get('name')

        if new_name and new_name != category.name:
            slug = await check_unique_slug(db=db, model=Category, name=new_name)
            setattr(category, 'slug', slug)

        for key, value in category_data_dict.items():
            setattr(category, key, value)

        await db.commit()
        await db.refresh(category)

        return category
