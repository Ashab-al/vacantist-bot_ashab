from fastapi_camelcase import CamelModel
from pydantic import Field


class DestroyCategoryRequest(CamelModel):
    """
    Схема запроса для удаления категории.

    Используется в API при передаче идентификатора категории,
    которую необходимо удалить из системы.
    """

    id: int = Field(
        ..., description="Уникальный идентификатор категории.", examples=[1]
    )
    """ID категории, которую требуется удалить."""
