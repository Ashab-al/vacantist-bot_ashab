from fastapi_camelcase import CamelModel
from pydantic import Field

class CreateCategoryRequest(CamelModel):
    """Схема для создания новой категории"""    
    name: str = Field(..., description='Название категории', examples=['Тех-спец'])