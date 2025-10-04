from fastapi_camelcase import CamelModel
from pydantic import Field

class ShowCategoryRequest(CamelModel):
    """
    Схема запроса API для получения информации о категории.

    Используется при передаче идентификатора категории,
    которую необходимо показать или получить из системы.
    """

    id: int = Field(
        ...,
        description="Уникальный идентификатор категории.",
        examples=[1]
    )
    """ID категории, информацию о которой нужно получить."""
