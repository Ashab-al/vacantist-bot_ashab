from fastapi_camelcase import CamelModel
from pydantic import Field

class UpdateCategoryRequest(CamelModel):
    """
    Схема запроса API для обновления категории.

    Используется при передаче новых данных категории, например, 
    для изменения её названия.
    """

    name: str = Field(
        ...,
        description="Новое название категории.",
        examples=["Тех-спец"]
    )
    """Новое название категории, которое необходимо установить."""
