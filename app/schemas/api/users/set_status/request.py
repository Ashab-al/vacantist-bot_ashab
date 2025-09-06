from fastapi_camelcase import CamelModel
from pydantic import Field
from enums.bot_status_enum import BotStatusEnum


class SetStatusUserIdRequest(CamelModel):
    """Схема для поиска пользователя"""    
    id: int = Field(..., description='id пользователя', examples=[1])

class SetStatusRequest(CamelModel):
    """Схема для поиска пользователя"""    
    bot_status: BotStatusEnum = Field(..., description='Статус пользователя в системе', examples=['works'])