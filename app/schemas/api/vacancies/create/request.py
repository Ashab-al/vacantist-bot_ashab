from fastapi_camelcase import CamelModel
from pydantic import Field


class CreateVacancyRequest(CamelModel):
    """Схема для создания новой вакансии"""
    title: str = Field(..., example="Технический специалист", description="Заголовок вакансии")
    category_title: str = Field(..., example="Тех-спец", description="Название категории к которому относится вакансия")
    description: str = Field(..., example="Описание вакансии", description="Описание вакансии")
    contact_information: str = Field(..., example="ТГ - @username", description="Контактные данные для связи")
    source: str = Field(..., example="telegram chat", description="Откуда прилетела вакансия")
    platform_id: int = Field(..., example=123123123, description="id отправителя")