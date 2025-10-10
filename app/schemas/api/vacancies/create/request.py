from fastapi_camelcase import CamelModel
from lib.tg.constants import SOURCE
from pydantic import Field


class CreateVacancyRequest(CamelModel):
    """
    Схема запроса API для создания новой вакансии.

    Используется для передачи данных о вакансии при её создании,
    включая заголовок, категорию, описание, контактную информацию
    и источник вакансии.
    """

    title: str = Field(
        ..., example="Технический специалист", description="Заголовок вакансии."
    )
    """Заголовок вакансии."""

    category_title: str = Field(
        ...,
        example="Тех-спец",
        description="Название категории, к которой относится вакансия.",
    )
    """Категория вакансии."""  # TODO Потом удалить. Посмотреть нужен ли на самом деле такой атрибут

    description: str = Field(
        ..., example="Описание вакансии", description="Подробное описание вакансии."
    )
    """Описание вакансии."""

    contact_information: str = Field(
        ...,
        example="ТГ - @username",
        description="Контактные данные для связи с отправителем вакансии.",
    )
    """Контактная информация."""

    source: str = Field(
        ..., example=SOURCE, description="Источник, откуда поступила вакансия."
    )
    """Источник вакансии."""

    platform_id: str = Field(
        ..., example="123123123", description="Идентификатор отправителя вакансии."
    )
    """ID платформы отправителя."""
