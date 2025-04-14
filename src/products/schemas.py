from typing import Annotated, Optional
from decimal import Decimal
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProductSchema(BaseModel):
    name: Annotated[str, Field(..., title='Название товара', min_length=2, max_length=255)]
    description: Annotated[Optional[str], Field(default="Нет описания", title='Описание товара', max_length=1000)]
    price: Annotated[Decimal, Field(ge=0, title='Цена товара')]
    image_url: Annotated[Optional[str], Field(title='URL картинки товара', description='URL для картинки товара')]
    stock: Annotated[int, Field(ge=0, title='Остаток товара')]
    rating: Annotated[float | int, Field(default=0, ge=0, le=5, title='Рейтинг товара')]
    category_id: Annotated[Optional[int], Field(default=None, title='ID категории', examples=[None, 1])]
    is_active: Annotated[bool, Field(default=True)]

    model_config = ConfigDict(from_attributes=True)

class ProductOutSchema(ProductSchema):
    id: Annotated[int, Field(..., title='ID', ge=0)]
    slug: Annotated[str, Field(..., title='slug', min_length=2, max_length=255)]
    created_at: Annotated[datetime, Field(..., title='Дата создания')]
    updated_at: Annotated[Optional[datetime], Field(title='Дата обновления')]

    model_config = ConfigDict(from_attributes=True)

