from fastapi_camelcase import CamelModel
from pydantic import Field, ConfigDict

class CreateCategoryResponse(CamelModel):
    """
    Схема ответа API после успешного создания категории.

    Используется для возврата клиенту данных о только что
    созданной категории, включая её уникальный идентификатор
    и название.
    """
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(
        ..., 
        example=1, 
        description="Уникальный идентификатор созданной категории."
    )
    """ID категории, сгенерированный базой данных."""

    name: str = Field(
        ..., 
        description="Название категории.", 
        examples=["Тех-спец"]
    )
    """Название категории, переданное при создании."""
