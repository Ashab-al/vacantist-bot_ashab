from fastapi_camelcase import CamelModel
from pydantic import Field

class ShowCategoryRequest(CamelModel):
    """Схема для возврата категории"""    
    id: int = Field(..., description='id категории', examples=[1])