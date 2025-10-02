from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User
from models.vacancy import Vacancy
from repositories.blacklist.black_list_check_by_platform_id_and_contact_information import black_list_check_by_platform_id_or_contact_information
from repositories.vacancies.find_vacancy_by_id import find_vacancy_by_id
from lib.tg.constants import SOURCE
from services.tg.spam_vacancy import COMPLAINT_COUNTER

REDUCE_BALANCE = 1
ZERO_BALANCE = 0
POINTS_EDGE = 5



async def open_vacancy(
    db: AsyncSession,
    user: User,
    vacancy_id: int        
) -> dict: 

    vacancy: Vacancy = await find_vacancy_by_id(db, vacancy_id)
    if not vacancy:
        raise ValueError(f"{vacancy_id} - такой вакансии нет в базе данных")
    
    return await check_vacancy(db, user, vacancy)

async def check_vacancy(
    db: AsyncSession,
    user: User,
    vacancy: Vacancy
) -> dict:
    if user.bonus + user.point <= ZERO_BALANCE:
        return {
            "status": "warning", 
            "path_view": "callback_query/out_of_points"
        }
    
    contact_information: str = vacancy.platform_id if vacancy.source == SOURCE else vacancy.contact_information

    if await check_blacklist(db, contact_information):
        return {
            "status": "warning", 
            "vacancy": vacancy, 
            "path_view": "callback_query/add_to_blacklist"
        }

    if user.bonus > ZERO_BALANCE:
        user.bonus = user.bonus - REDUCE_BALANCE
    else:
        user.point = user.point - REDUCE_BALANCE

    await db.commit()
    await db.refresh(user)
    await db.refresh(vacancy)

    return {
        "status": "open_vacancy",
        "vacancy": vacancy,
        "path_view": "callback_query/open_vacancy",
        "low_points": user.point <= POINTS_EDGE
    }

async def check_blacklist(
    db: AsyncSession,
    contact_information: str
):
    blacklist = await black_list_check_by_platform_id_or_contact_information(
        db,
        contact_information=contact_information    
    )

    return (blacklist and blacklist.complaint_counter >= COMPLAINT_COUNTER)