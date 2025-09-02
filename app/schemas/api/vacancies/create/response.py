from fastapi_camelcase import CamelModel
from pydantic import Field

class CreateVacancyResponse(CamelModel):
    """Схема для возврата успешного ответа после создания вакансии"""

    id: int = Field(..., example=1, description="id созданной вакансии")
    title: str = Field(..., example="Технический специалист", description="Заголовок созданной вакансии")
    description: str = Field(..., example="Описание вакансии", description="Описание вакансии")
    contact_information: str = Field(..., example="ТГ - @username", description="Контактные данные для связи")
    source: str = Field(..., example="telegram chat", description="Откуда прилетела вакансия")
    platform_id: str = Field(..., example='123123123', description="id отправителя")
    category_title: str = Field(..., example="Тех-спец", description="Название категории к которому относится вакансия")