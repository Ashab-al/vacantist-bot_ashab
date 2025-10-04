from fastapi_camelcase import CamelModel
from pydantic import Field

class CreateCategoryRequest(CamelModel):
    """
    Схема запроса для создания новой категории.

    Используется в API при отправке данных для добавления
    новой категории в систему.
    """    

    name: str = Field(
        ..., 
        description="Название категории. Должно быть уникальным и отражать суть категории.", 
        examples=["Тех-спец"]
    )
    """Название категории, передаваемое клиентом в запросе."""
