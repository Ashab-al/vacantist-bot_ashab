from fastapi_camelcase import CamelModel
from pydantic import Field, ConfigDict
from datetime import datetime

class CategoryResponse(CamelModel):
    """Схема для возврата категории"""
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="id категории", example=1)
    name: str = Field(..., description='Название категории', examples=['Тех-спец'])
    created_at: datetime = Field(..., description='Дата создания категории')
    updated_at: datetime = Field(..., description='Дата последнего обновления категории')

class ListCategoryResponse(CamelModel):
    """Схема для возврата списка категорий"""

    categories: list[CategoryResponse] = Field(..., description='Список категорий')