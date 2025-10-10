from fastapi_camelcase import CamelModel
from pydantic import Field


class CreateVacancyResponse(CamelModel):
    """
    Схема ответа API после успешного создания вакансии.

    Используется для возврата данных о созданной вакансии,
    включая идентификатор, заголовок, описание, контактную информацию,
    источник и категорию.
    """

    id: int = Field(
        ..., examples=[1], description="Уникальный идентификатор созданной вакансии."
    )
    """ID созданной вакансии."""

    title: str = Field(
        ...,
        examples=["Технический специалист"],
        description="Заголовок созданной вакансии.",
    )
    """Заголовок вакансии."""

    description: str = Field(
        ..., examples=["Описание вакансии"], description="Подробное описание вакансии."
    )
    """Описание вакансии."""

    contact_information: str = Field(
        ...,
        examples=["ТГ - @username"],
        description="Контактные данные для связи с отправителем вакансии.",
    )
    """Контактная информация."""

    source: str = Field(
        ..., examples=["telegram chat"], description="Источник, откуда поступила вакансия."
    )
    """Источник вакансии."""

    platform_id: str = Field(
        ..., examples=["123123123"], description="Идентификатор отправителя вакансии."
    )
    """ID платформы отправителя."""

    category_title: str = Field(
        ...,
        examples=["Тех-спец"],
        description="Название категории, к которой относится вакансия.",
    )
    """Категория вакансии."""
