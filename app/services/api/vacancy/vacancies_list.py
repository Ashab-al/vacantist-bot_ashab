from models.vacancy import Vacancy
from schemas.api.vacancies.vacancy import VacancySchema
from repositories.vacancies.get_all_vacancies import get_all_vacancies
from sqlalchemy.ext.asyncio import AsyncSession

async def vacancies_list(
    db: AsyncSession
) -> list[VacancySchema]:
    vacancies: list[VacancySchema] = await get_all_vacancies(db)
    
    vacancies_to_schema: list[VacancySchema] = [
        VacancySchema.model_validate(vacancy)
        for vacancy in vacancies
    ]

    return vacancies_to_schema