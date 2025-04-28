from typing import Annotated, Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class CategorySchema(BaseModel):
    name: Annotated[str, Field(max_length=255, title="Название категории")]
    parent_id: Annotated[
        Optional[int],
        Field(
            default=None, ge=0, title="ID родительской категории", examples=[None, 1]
        ),
    ]

    model_config = ConfigDict(from_attributes=True)


class CategoryOutSchema(CategorySchema):
    id: Annotated[int, Field(..., title="ID", ge=0)]
    slug: Annotated[str, Field(..., title="slug", min_length=2, max_length=255)]
    created_at: Annotated[datetime, Field(..., title="Дата создания")]
    updated_at: Annotated[Optional[datetime], Field(title="Дата обновления")]
