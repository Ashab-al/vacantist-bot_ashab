from fastapi_camelcase import CamelModel
from pydantic import Field


class SetBonusUserIdRequest(CamelModel):
    """Схема для поиска пользователя"""    
    id: int = Field(..., description='id пользователя', examples=[1])

class SetBonusRequest(CamelModel):
    """Схема для обновления количество бонусов у пользователя"""    
    count: int = Field(..., ge=0, examples=[10], description='Количество бонусов')