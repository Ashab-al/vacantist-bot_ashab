from fastapi_camelcase import CamelModel
from pydantic import Field, ConfigDict

class CreateCategoryResponse(CamelModel):
    """Схема для возврата успешного ответа после создании категории"""
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., example=1, description="id созданной категории")
    name: str = Field(..., description='Название категории', examples=['Тех-спец'])