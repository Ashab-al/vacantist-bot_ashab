# pylint: disable=duplicate-code
from fastapi_camelcase import CamelModel
from pydantic import Field


class SetBonusUserIdRequest(CamelModel):
    """
    Схема запроса API для указания пользователя, которому будут
    начислены бонусы.

    Используется для передачи идентификатора пользователя.
    """

    id: int = Field(
        ..., description="Уникальный идентификатор пользователя.", examples=[1]
    )
    """ID пользователя, для которого будут установлены бонусы."""


class SetBonusRequest(CamelModel):
    """
    Схема запроса API для обновления количества бонусов у пользователя.

    Используется для передачи нового значения бонусов.
    """

    count: int = Field(
        ..., ge=0, description="Количество бонусов для пользователя.", examples=[10]
    )
    """Новое количество бонусов пользователя (должно быть >= 0)."""
