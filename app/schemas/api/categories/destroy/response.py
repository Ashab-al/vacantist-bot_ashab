from fastapi_camelcase import CamelModel
from pydantic import Field, ConfigDict
from datetime import datetime


class DestroyCategoryResponse(CamelModel):
    """Схема для возврата успешного ответа после удаления категории"""
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="id категории", example=1)
    name: str = Field(..., description='Название категории', examples=['Тех-спец'])
    created_at: datetime = Field(..., description='Дата создания категории')
    updated_at: datetime = Field(..., description='Дата последнего обновления категории')