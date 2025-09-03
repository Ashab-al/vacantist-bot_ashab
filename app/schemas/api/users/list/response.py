from fastapi_camelcase import CamelModel
from pydantic import Field, ConfigDict, computed_field
from datetime import datetime
from enums.bot_status_enum import BotStatusEnum


class UserResponse(CamelModel):
    """Схема для возврата Пользователей"""
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

    @computed_field(
        return_type=list[str],
        description='Список категорий пользователя',
        examples=[['Тех-спец', 'SMM']]
    )
    def categories(self) -> list[str]:
        categories: list[str] = []
        
        for category in self.categories:
            categories.append(category.name)
        return categories


class ListUsersResponse(CamelModel):
    """Схема для возврата списка категорий"""

    users: list[UserResponse] = Field(..., description='Список пользователей')