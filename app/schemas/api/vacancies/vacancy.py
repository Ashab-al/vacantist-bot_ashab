from fastapi_camelcase import CamelModel
from pydantic import Field, ConfigDict, computed_field


class VacancySchema(CamelModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., example=1, description="id созданной вакансии")
    title: str = Field(..., example="Технический специалист", description="Заголовок созданной вакансии")
    description: str = Field(..., example="Описание вакансии", description="Описание вакансии")
    contact_information: str = Field(..., example="ТГ - @username", description="Контактные данные для связи")
    source: str = Field(..., example="telegram chat", description="Откуда прилетела вакансия")
    platform_id: str = Field(..., example='123123123', description="id отправителя")

    category: object | None = Field(None, exclude=True)

    @computed_field(
        return_type=str,
        description='Название категории к которому относится вакансия', 
        examples=['Тех-спец']
    )
    def category_title(self) -> str:
        return self.category.name