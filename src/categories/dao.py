from sqlalchemy.ext.asyncio import AsyncSession

from src.categories.models import Category
from src.categories.schemas import CategorySchema
from src.dao.base_dao import BaseDao
from src.dependecies.dependencies import check_unique_slug
from src.users.models import User
from src.users.dependencies import check_is_admin


class CategoryDAO(BaseDao):
    model = Category

    @classmethod
    async def create_category(cls, db: AsyncSession, user: User, new_category: CategorySchema) -> Category:
        check_is_admin(user)
        slug = await check_unique_slug(name=new_category.name, model=cls.model, db=db)
        category = await cls.create(db=db, **new_category.model_dump(), slug=slug)

        return category

    @classmethod
    async def update_category(cls,
                              db: AsyncSession,
                              user: User,
                              category_data: CategorySchema,
                              category: Category) -> Category:
        check_is_admin(user)
        data = category_data.model_dump(exclude_unset=True)

        if 'name' in data and data['name'] != category.name:
            data['slug'] = await check_unique_slug(db=db, model=cls.model, name=data['name'])

        updated_category = await cls.update(db=db, instance=category, **data)

        return updated_category
