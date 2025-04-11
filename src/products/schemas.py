from typing import Annotated, Optional
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field


class ProductSchema(BaseModel):
    name: Annotated[str, Field(title='Название товара', min_length=1, max_length=255)]
    description: Annotated[Optional[str], Field(default="Нет описания", title='Описание товара', max_length=1000)]
    price: Annotated[int, Field(ge=0, title='Цена товара')]
    image_url: Annotated[Optional[str], Field(title='URL картинки товара', description='URL для картинки товара')]
    stock: Annotated[int, Field(ge=0, title='Остаток товара')]
    rating: Annotated[float | int, Field(default=0, title='Рейтинг товара')]
    category_id: Annotated[Optional[int], Field(ge=0, title='ID категории')]

    model_config = ConfigDict(from_attributes=True)

