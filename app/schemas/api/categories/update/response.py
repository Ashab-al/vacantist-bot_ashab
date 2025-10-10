from datetime import datetime

from fastapi_camelcase import CamelModel
from pydantic import ConfigDict, Field


class UpdateCategoryResponse(CamelModel):
    """
    Схема ответа API после обновления категории.

    Используется для передачи клиенту актуальной информации о категории,
    включая её идентификатор, название и временные метки создания и обновления.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Уникальный идентификатор категории.", examples=[1])
    """ID категории."""

    name: str = Field(..., description="Название категории.", examples=["Тех-спец"])
    """Название категории."""

    created_at: datetime = Field(..., description="Дата и время создания категории.")
    """Временная метка создания категории."""

    updated_at: datetime = Field(
        ..., description="Дата и время последнего обновления категории."
    )
    """Временная метка последнего обновления категории."""
