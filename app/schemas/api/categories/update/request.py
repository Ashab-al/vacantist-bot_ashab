from fastapi_camelcase import CamelModel
from pydantic import Field

class UpdateCategoryRequest(CamelModel):
    """Схема для обновления категории"""    
    name: str = Field(..., description='Новое название категории', examples=['Тех-спец'])