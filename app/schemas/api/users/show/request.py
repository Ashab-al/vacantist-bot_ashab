from fastapi_camelcase import CamelModel
from pydantic import Field

class ShowUserRequest(CamelModel):
    """Схема для поиска пользователя"""    
    id: int = Field(..., description='id пользователя', examples=[1])