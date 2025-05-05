from datetime import datetime
from decimal import Decimal
from typing import Annotated, Optional

from pydantic import BaseModel, Field, ConfigDict

from src.orders.models import OrderEnum


class OrderItemSchema(BaseModel):
    product_slug: Annotated[str, Field(..., title="slug", min_length=2, max_length=255, description="slug товара")]
    quantity: Annotated[int, Field(default=1, gt=0, description="Количество товара в заказе")]

    model_config = ConfigDict(from_attributes=True)


class OrderItemOutSchema(OrderItemSchema):
    id: Annotated[int, Field(..., gt=0, description="Уникальный ID позиции в заказе")]
    order_id: Annotated[int, Field(..., gt=0, description="ID заказа")]
    product_name_snapshot: Annotated[str, Field(..., max_length=255, description="Название продукта")]
    price_at_time: Annotated[
        Decimal, Field(..., max_digits=10, decimal_places=2, description="Цена товара в момент заказа")]

    model_config = ConfigDict(from_attributes=True)


class OrderCreateSchema(BaseModel):
    order_items: list[OrderItemSchema]

    model_config = ConfigDict(from_attributes=True)


class OrderShortOutSchema(BaseModel):
    id: Annotated[int, Field(..., gt=0, description="ID заказа")]
    total_price: Annotated[Decimal, Field(..., ge=0, max_digits=10, decimal_places=2, description="Сумма заказа")]
    status: Annotated[OrderEnum, Field(..., description="Статус заказа")]
    created_at: Annotated[datetime, Field(..., title="Дата создания заказа")]
    updated_at: Annotated[Optional[datetime], Field(default=None, title="Дата обновления заказа")]
    user_id: Annotated[int, Field(..., gt=0, description="ID пользователя")]

    model_config = ConfigDict(from_attributes=True)


class OrderOutSchema(OrderShortOutSchema):
    order_items: list[OrderItemOutSchema]
