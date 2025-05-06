from datetime import datetime
from decimal import Decimal
from typing import Annotated, Optional

from pydantic import Field, BaseModel, ConfigDict


class CartSchema(BaseModel):
    id: Annotated[int, Field(..., gt=0, description='ID корзины')]
    user_id: Annotated[int, Field(..., gt=0, description='ID пользователя')]
    updated_at: Annotated[Optional[datetime], Field(default=None, title="Дата и время обновления корзины")]

    model_config = ConfigDict(from_attributes=True)


class CartItemSchema(BaseModel):
    id: Annotated[int, Field(..., description='ID позиции в корзине')]
    cart_id: Annotated[int, Field(..., description='ID корзины')]
    product_slug: Annotated[str, Field(..., description='Slug товара')]
    product_name_snapshot: Annotated[str, Field(..., max_length=255, description="Название товара")]
    price_at_time: Annotated[
        Decimal, Field(..., max_digits=10, decimal_places=2, description="Цена товара в момент добавления в корзину")]
    quantity: Annotated[int, Field(default=1, ge=0, description="Количество товара в корзине")]

    created_at: Annotated[datetime, Field(..., title="Дата и время добавления товара")]
    updated_at: Annotated[Optional[datetime], Field(default=None, title="Дата и время обновления товара")]

    model_config = ConfigDict(from_attributes=True)


class CartOutSchema(CartSchema):
    cart_items: list[CartItemSchema]

    model_config = ConfigDict(from_attributes=True)


class CartItemChangeSchema(BaseModel):
    product_slug: Annotated[str, Field(..., description='Slug товара')]
    quantity: Annotated[int, Field(default=1, ge=0, description="Количество товара для добавления в корзину")]

    model_config = ConfigDict(from_attributes=True)
