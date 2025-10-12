# pylint: disable=duplicate-code
from datetime import datetime

from fastapi_camelcase import CamelModel
from pydantic import ConfigDict, Field


class DestroyCategoryResponse(CamelModel):
    """
    Схема ответа API после успешного удаления категории.

    Используется для возврата клиенту информации о категории,
    которая была удалена, включая её идентификатор, название
    и временные метки создания и обновления.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(
        ..., description="Уникальный идентификатор категории.", examples=[1]
    )
    """ID категории, удалённой из системы."""

    name: str = Field(..., description="Название категории.", examples=["Тех-спец"])
    """Название удалённой категории."""

    created_at: datetime = Field(..., description="Дата и время создания категории.")
    """Метка времени, когда категория была создана."""

    updated_at: datetime = Field(
        ..., description="Дата и время последнего обновления категории."
    )
    """Метка времени последнего обновления перед удалением."""
