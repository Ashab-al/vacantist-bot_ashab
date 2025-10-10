from datetime import datetime

from fastapi_camelcase import CamelModel
from pydantic import ConfigDict, Field


class CategoryResponse(CamelModel):
    """
    Схема ответа API с данными категории.

    Используется для возврата информации о категории,
    включая её уникальный идентификатор, название и временные метки.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Уникальный идентификатор категории.", example=1)
    """ID категории."""

    name: str = Field(..., description="Название категории.", examples=["Тех-спец"])
    """Название категории."""

    created_at: datetime = Field(..., description="Дата и время создания категории.")
    """Метка времени, когда категория была создана."""

    updated_at: datetime = Field(
        ..., description="Дата и время последнего обновления категории."
    )
    """Метка времени последнего обновления категории."""


class ListCategoryResponse(CamelModel):
    """
    Схема ответа API для возврата списка категорий.

    Содержит коллекцию объектов `CategoryResponse`.
    """

    categories: list[CategoryResponse] = Field(..., description="Список категорий.")
    """Список категорий."""
