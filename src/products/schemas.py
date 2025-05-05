from datetime import datetime
from decimal import Decimal
from typing import Annotated, Optional

from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field

from src.categories.schemas import CategoryOutSchema


class ProductSchema(BaseModel):
    name: Annotated[
        str, Field(..., title="Название товара", min_length=2, max_length=255)
    ]
    description: Annotated[
        Optional[str], Field(default=None, title="Описание товара", max_length=1000)
    ]
    price: Annotated[Decimal, Field(ge=0, title="Цена товара")]
    image_url: Annotated[Optional[str], Field(title="URL картинки товара")]
    stock: Annotated[int, Field(ge=0, title="Остаток товара")]
    rating: Annotated[float | int, Field(default=0, ge=0, le=5, title="Рейтинг товара")]
    category_id: Annotated[
        Optional[int], Field(default=None, title="ID категории", examples=[None, 1])
    ]
    is_active: Annotated[bool, Field(default=True)]

    model_config = ConfigDict(from_attributes=True)


class ProductOutSchema(ProductSchema):
    id: Annotated[int, Field(..., title="ID", ge=0)]
    slug: Annotated[str, Field(..., title="slug", min_length=2, max_length=255)]
    created_at: Annotated[datetime, Field(..., title="Дата создания")]
    updated_at: Annotated[
        Optional[datetime], Field(default=None, title="Дата обновления")
    ]
    category: Annotated[CategoryOutSchema | None, Field(default=None, title="Категория")]
    model_config = ConfigDict(from_attributes=True)


class ProductFilters:
    def __init__(
        self,
        name: Optional[str] = Query(
            None, description="Фильтр по названию (частичное совпадение)"
        ),
        min_price: Optional[Decimal] = Query(None, description="Минимальная цена"),
        max_price: Optional[Decimal] = Query(None, description="Максимальная цена"),
        category_slug: Optional[str] = Query(None, description="Slug категории"),
        in_stock: Optional[bool] = Query(None, description="Только товары в наличии"),
        is_active: Optional[bool] = Query(
            True, description="Только активные товары (по умолчанию True)"
        ),
        min_rating: Optional[float] = Query(
            None, ge=0, le=5, description="Минимальный рейтинг (от 0 до 5)"
        ),
    ):
        self.name = name
        self.min_price = min_price
        self.max_price = max_price
        self.category_slug = category_slug
        self.in_stock = in_stock
        self.is_active = is_active
        self.min_rating = min_rating


class ProductUpdateSchema(BaseModel):
    name: Annotated[
        Optional[str],
        Field(
            default=None,
            title="Название товара",
            min_length=2,
            max_length=255,
            example="iPhone 14",
        ),
    ]
    description: Annotated[
        Optional[str],
        Field(
            default=None,
            title="Описание товара",
            max_length=1000,
            example="Современный смартфон от Apple",
        ),
    ]
    price: Annotated[
        Optional[Decimal],
        Field(default=None, ge=0, title="Цена товара", example=799.99),
    ]
    image_url: Annotated[
        Optional[str],
        Field(
            default=None,
            title="URL картинки товара",
            example="https://example.com/image.png",
        ),
    ]
    stock: Annotated[
        Optional[int], Field(default=None, ge=0, title="Остаток товара", example=10)
    ]
    rating: Annotated[
        Optional[float],
        Field(default=None, ge=0, le=5, title="Рейтинг товара", example=4.8),
    ]
    category_id: Annotated[
        Optional[int], Field(default=None, title="ID категории", example=1)
    ]
    is_active: Annotated[
        Optional[bool], Field(default=None, title="Активен ли товар", example=True)
    ]

    model_config = ConfigDict(from_attributes=True)
