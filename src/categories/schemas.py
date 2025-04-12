from typing import Annotated
from pydantic import BaseModel, Field


class CategorySchema(BaseModel):
    name: Annotated[str, Field(max_length=255, title='Название категории')]
