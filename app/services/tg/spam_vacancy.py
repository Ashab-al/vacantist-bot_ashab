from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User
from models.vacancy import Vacancy
from models.blacklist import BlackList
from repositories.blacklist.black_list_check_by_platform_id_and_contact_information import black_list_check_by_platform_id_or_contact_information
from repositories.vacancies.find_vacancy_by_id import find_vacancy_by_id
from lib.tg.constants import SOURCE


COMPLAINT_COUNTER = 2
BLACKLISTED = "blacklisted"

async def spam_vacancy(
    db: AsyncSession,
    vacancy_id: int        
):
    vacancy: Vacancy = await find_vacancy_by_id(db, vacancy_id)
    contact_information: str = vacancy.platform_id if vacancy.source == SOURCE else vacancy.contact_information

    blacklist: BlackList = await black_list_check_by_platform_id_or_contact_information(
        db, 
        contact_information=contact_information
    )
    zero = 0
    if not blacklist:
        blacklist: BlackList = BlackList(
            contact_information=contact_information,
            complaint_counter=zero
        )
        db.add(blacklist)
        await db.commit()
        await db.refresh(blacklist)
    
    if blacklist.complaint_counter >= COMPLAINT_COUNTER:
        return BLACKLISTED
    
    blacklist.complaint_counter += 1
    await db.commit()
    await db.refresh(blacklist)
