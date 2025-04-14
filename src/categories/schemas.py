from typing import Annotated, Optional
from pydantic import BaseModel, Field, ConfigDict


class CategorySchema(BaseModel):
    name: Annotated[str, Field(max_length=255, title='Название категории')]
    parent_id: Annotated[Optional[int], Field(default=None, max_length=255, title='ID родительской категории', examples=[None, 1])]

    model_config = ConfigDict(from_attributes=True)