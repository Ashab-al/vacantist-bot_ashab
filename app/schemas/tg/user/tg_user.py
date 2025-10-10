from enums.bot_status_enum import BotStatusEnum
from fastapi_camelcase import CamelModel
from models.user import User
from pydantic import ConfigDict, Field


class TgUser(CamelModel):
    """
    Схема пользователя Telegram.

    Используется для возврата информации о пользователе Telegram,
    включая идентификатор, имя, username, поинты, бонусы, статус
    и контактные данные.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(
        ...,
        description="Уникальный идентификатор пользователя в Telegram.",
        examples=[1],
        alias="platform_id",
    )
    """ID пользователя в Telegram."""

    first_name: str = Field(..., description="Имя пользователя.", examples=["Асхаб"])
    """Имя пользователя."""

    username: str | None = Field(
        None, description="Username пользователя в Telegram.", examples=["ashabal"]
    )
    """Telegram username пользователя, если указан."""

    point: int = Field(
        default=User.DEFAULT_POINT,
        description="Количество поинтов пользователя.",
        examples=[10],
    )
    """Количество обычных поинтов пользователя."""

    bonus: int = Field(
        default=User.DEFAULT_BONUS,
        description="Количество бонусных поинтов пользователя.",
        examples=[10],
    )
    """Количество бонусных поинтов пользователя."""

    bot_status: BotStatusEnum = Field(
        default=BotStatusEnum.WORKS,
        description="Статус пользователя в системе.",
        examples=["WORKS", "BOT_BLOCKED"],
    )
    """Статус пользователя (например, WORKS или BOT_BLOCKED)."""

    email: str | None = Field(
        None, description="Email пользователя.", examples=["test@gmail.com"]
    )
    """Почта пользователя, если указана."""

    phone: str | None = Field(
        None, description="Телефон пользователя.", examples=["79287804986"]
    )
    """Телефон пользователя, если указан."""
