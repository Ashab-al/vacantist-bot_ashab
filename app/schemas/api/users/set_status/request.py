from fastapi_camelcase import CamelModel
from pydantic import Field
from enums.bot_status_enum import BotStatusEnum


class SetStatusUserIdRequest(CamelModel):
    """
    Схема запроса API для указания пользователя, чей статус будет изменён.

    Используется для передачи идентификатора пользователя.
    """
    id: int = Field(
        ...,
        description="Уникальный идентификатор пользователя.",
        examples=[1]
    )
    """ID пользователя, для которого будет установлен новый статус."""


class SetStatusRequest(CamelModel):
    """
    Схема запроса API для обновления `bot_status` пользователя.

    Используется для передачи нового статуса пользователя в системе.
    """
    bot_status: BotStatusEnum = Field(
        ...,
        description="Статус пользователя в системе.",
        examples=[BotStatusEnum.WORKS, BotStatusEnum.BOT_BLOCKED]
    )
    """Новый статус пользователя (например, WORKS или BOT_BLOCKED)."""
