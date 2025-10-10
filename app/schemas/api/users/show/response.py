from fastapi_camelcase import CamelModel
from pydantic import Field, ConfigDict
from datetime import datetime
from enums.bot_status_enum import BotStatusEnum
from schemas.api.categories.list.response import CategoryResponse


class ShowUserResponse(CamelModel):
    """
    Схема ответа API с данными пользователя.

    Используется для возврата информации о пользователе, включая идентификаторы,
    контактные данные, поинты и бонусы, статус в системе и связанные категории.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(
        ..., description="Уникальный идентификатор пользователя.", example=1
    )
    """ID пользователя в системе."""

    platform_id: int = Field(
        ...,
        description="Идентификатор пользователя в Telegram.",
        examples=[12312312312],
    )
    """Telegram platform_id пользователя."""

    first_name: str = Field(..., description="Имя пользователя.", examples=["Асхаб"])
    """Имя пользователя."""

    username: str = Field(
        ..., description="Username пользователя в Telegram.", examples=["ashabal"]
    )
    """Telegram username пользователя."""

    email: str | None = Field(
        None, description="Email пользователя.", examples=["asxabal7@gmail.com"]
    )
    """Email пользователя, если указан."""

    phone: str | None = Field(
        None, description="Телефон пользователя.", examples=["79999999999"]
    )
    """Телефон пользователя, если указан."""

    point: int = Field(
        ..., description="Количество поинтов пользователя.", examples=[10]
    )
    """Количество поинтов пользователя."""

    bonus: int = Field(
        ..., description="Количество бонусных поинтов пользователя.", examples=[10]
    )
    """Количество бонусных поинтов пользователя."""

    bot_status: BotStatusEnum = Field(
        ..., description="Статус пользователя в системе.", examples=["works"]
    )
    """Статус пользователя в системе (например, WORKS или BOT_BLOCKED)."""

    created_at: datetime = Field(..., description="Дата и время создания пользователя.")
    """Метка времени создания пользователя."""

    updated_at: datetime = Field(
        ..., description="Дата и время последнего обновления пользователя."
    )
    """Метка времени последнего обновления пользователя."""

    categories: list[CategoryResponse] = Field(
        ..., description="Список категорий пользователя."
    )
    """Список категорий, связанных с пользователем."""
