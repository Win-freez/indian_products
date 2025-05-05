from pydantic import Field, BaseModel
from typing import Annotated
from decimal import Decimal


class CartItemSchema(BaseModel):
    id: Annotated[int, Field(..., description='ID позиции в корзине')]
    cart_id: Annotated[int, Field(..., description='ID корзины')]
    product_slug: Annotated[str, Field(..., description='Slug товара')]
    product_name_snapshot: Annotated[str, Field(..., max_length=255, description="Название товара")]
    price_at_time: Annotated[
        Decimal, Field(..., max_digits=10, decimal_places=2, description="Цена товара в момент добавления в корзину")]
    quantity: Annotated[int, Field(default=1, gt=0, description="Количество товара в корзине")]


class CartSchema(BaseModel):
    id: Annotated[int, Field(..., gt=0, description='ID корзины')]
    user_id: Annotated[int, Field(..., gt=0, description='ID пользователя')]
    cart_items: list[CartItemSchema]
    total_price: Annotated[Decimal, Field(..., max_digits=10, decimal_places=2, description="Общая стоимость корзины")]


class CartItemAddSchema(BaseModel):
    product_slug: Annotated[str, Field(..., description='Slug товара')]
    quantity: Annotated[int, Field(default=1, gt=0, description="Количество товара для добавления в корзину")]
