from fastapi_camelcase import CamelModel
from pydantic import Field, ConfigDict, computed_field


class VacancySchema(CamelModel):
    """
    Схема данных вакансии.

    Используется для возврата информации о вакансии, включая
    идентификатор, заголовок, описание, контактные данные,
    источник, отправителя и категорию.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., example=1, description="Уникальный идентификатор вакансии.")
    """ID созданной вакансии."""

    title: str = Field(
        ..., example="Технический специалист", description="Заголовок вакансии."
    )
    """Заголовок вакансии."""

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

    source: str = Field(..., example="telegram chat", description="Источник вакансии.")
    """Источник вакансии."""

    platform_id: str = Field(
        ..., example="123123123", description="Идентификатор отправителя вакансии."
    )
    """ID платформы отправителя."""

    category: object | None = Field(None, exclude=True)
    """Объект категории, к которой относится вакансия (не включается в сериализацию)."""

    @computed_field(
        return_type=str,
        description="Название категории, к которой относится вакансия.",
        examples=["Тех-спец"],
    )
    def category_title(self) -> str:
        """Возвращает название категории вакансии."""
        return self.category.name
