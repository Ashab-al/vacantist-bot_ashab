from fastapi_camelcase import CamelModel
from pydantic import Field
from schemas.api.vacancies.vacancy import VacancySchema


class ListVacancyResponse(CamelModel):
    """Схема для возврата успешного ответа списка вакансий"""
    vacancies: list[VacancySchema] = Field(
        ..., 
        description='Список вакансий', 
        example=[
            {
                "id": 1,
                "title": "Технический специалист",
                "category_title": "Тех-спец",
                "description": "Описание вакансии 1",
                "contact_information": "ТГ - @username",
                "source": "telegram chat",
                "platform_id": "123123123"
            },
            {
                "id": 2,
                "title": "Копирайт",
                "category_title": "Копирайт",
                "description": "Описание вакансии 2",
                "contact_information": "ТГ - @username",
                "source": "telegram chat",
                "platform_id": "123123123"
            }
        ]
    )
    count: int = Field(..., description='Общее количество найденных вакансий', example=2)