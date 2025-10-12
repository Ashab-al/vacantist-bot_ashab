from repositories.vacancies.get_all_vacancies import get_all_vacancies
from schemas.api.vacancies.vacancy import VacancySchema
from sqlalchemy.ext.asyncio import AsyncSession


async def vacancies_list(db: AsyncSession) -> list[VacancySchema]:
    """
    Возвращает список всех вакансий

    Args:
        db (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных

    Returns:
        list[VacancySchema]: Список вакансий, представленных в виде схем Pydantic.
    """
    return [
        VacancySchema.model_validate(vacancy) for vacancy in await get_all_vacancies(db)
    ]
