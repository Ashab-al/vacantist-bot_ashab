# pylint: disable=duplicate-code
from fastapi_camelcase import CamelModel
from pydantic import Field


class ShowUserRequest(CamelModel):
    """
    Схема запроса API для получения информации о пользователе.

    Используется для передачи идентификатора пользователя,
    информацию о котором необходимо вернуть.
    """

    id: int = Field(
        ..., description="Уникальный идентификатор пользователя.", examples=[1]
    )
    """ID пользователя, информацию о котором необходимо получить."""
