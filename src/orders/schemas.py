from decimal import Decimal
from typing import Annotated
from pydantic import BaseModel, Field, ConfigDict

from src.orders.models import OrderEnum


class OrderItemSchema(BaseModel):
    product_id: Annotated[int, Field(..., ge=0, description='ID товара')]
    quantity: Annotated[int, Field(default=1, gt=0, description='Количество товара')]
    price_at_time: Annotated[Decimal, Field(..., ge=0, description='Цена товара на момент покупки')]

    model_config = ConfigDict(from_attributes=True)

class OrderSchema(BaseModel):
    user_id: Annotated[int, Field(..., ge=0, description='ID пользователя')]
    total_price: Annotated[Decimal, Field(..., ge=0, description='Сумма заказа')]
    status: Annotated[OrderEnum, Field(..., description='Статус заказа')]
    items: list[OrderItemSchema]

    model_config = ConfigDict(from_attributes=True)