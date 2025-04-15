from typing import Annotated, Optional
from decimal import Decimal
from datetime import datetime

from fastapi import Query
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


class ProductFilters:
    def __init__(
            self,
            name: Optional[str] = Query(None, description="Фильтр по названию (частичное совпадение)"),
            min_price: Optional[Decimal] = Query(None, description="Минимальная цена"),
            max_price: Optional[Decimal] = Query(None, description="Максимальная цена"),
            category_slug: Optional[str] = Query(None, description="Slug категории"),
            in_stock: Optional[bool] = Query(None, description="Только товары в наличии"),
            is_active: Optional[bool] = Query(True, description="Только активные товары (по умолчанию True)"),
            min_rating: Optional[float] = Query(None, ge=0, le=5, description="Минимальный рейтинг (от 0 до 5)"),
    ):
        self.name = name
        self.min_price = min_price
        self.max_price = max_price
        self.category_slug = category_slug
        self.in_stock = in_stock
        self.is_active = is_active
        self.min_rating = min_rating

class ProductUpdatePartialSchema(BaseModel):
    pass