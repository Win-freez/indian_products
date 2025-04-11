from typing import Annotated
from pydantic import BaseModel, Field


class CategorySchema(BaseModel):
    id: Annotated[int, Field(ge=0, title='ID категории')]
    name: Annotated[str, Field(max_length=255, title='Название категории')]
