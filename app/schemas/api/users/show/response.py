from fastapi_camelcase import CamelModel
from pydantic import Field, ConfigDict, computed_field
from datetime import datetime
from enums.bot_status_enum import BotStatusEnum
from schemas.api.categories.list.response import CategoryResponse

class ShowUserResponse(CamelModel):
    """Схема для возврата Пользователя"""
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="id пользователя", example=1)
    platform_id: int = Field(..., description="id пользователя в telegram", examples=[ 12312312312 ])
    first_name: str = Field(..., description='Имя пользователя', examples=['Асхаб'])
    username: str = Field(..., description='username пользователя в telegram', examples=['ashabal'])
    email: str | None = Field(None, description='Email пользователя', examples=['asxabal7@gmail.com'])
    phone: str | None = Field(None, description='Телефон пользователя', examples=['79999999999'])
    point: int = Field(..., description='Количество поинтов у пользователя', examples=[10])
    bonus: int = Field(..., description='Количество бонусных поинтов у пользователя', examples=[10])
    bot_status: BotStatusEnum = Field(..., description='Статус пользователя в системе', examples=['works'])
    created_at: datetime = Field(..., description='Дата создания пользователя')
    updated_at: datetime = Field(..., description='Дата последнего обновления пользователя')

    categories: list[CategoryResponse] = Field(..., description='Список категорий')