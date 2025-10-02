from fastapi_camelcase import CamelModel
from pydantic import Field, ConfigDict, computed_field
from datetime import datetime
from enums.bot_status_enum import BotStatusEnum
from schemas.api.categories.list.response import CategoryResponse
from models.user import User

class TgUser(CamelModel):
    """Схема для Пользователя телеграм"""
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="id пользователя в телеграм", example=1, alias='platform_id')
    first_name: str = Field(..., description='Имя пользователя', examples=['Асхаб'])
    username: str | None = Field(None, description='username пользователя в telegram', examples=['ashabal'])
    point: int = Field(default=User.DEFAULT_POINT, description='Количество поинтов у пользователя', examples=[10])
    bonus: int = Field(default=User.DEFAULT_BONUS, description='Количество бонусных поинтов у пользователя', examples=[10])
    bot_status: BotStatusEnum = Field(default=BotStatusEnum.WORKS, description='Статус пользователя в системе', examples=['WORKS', 'BOT_BLOCKED'])
    email: str | None = Field(None, description="Почта пользователя", examples=['test@gmail.com'])
    phone: str | None = Field(None, description="Телефон пользователя", examples=['79287804986'])