from sqlalchemy.ext.asyncio import AsyncSession
from models.blacklist import BlackList
from repositories.blacklist.black_list_check_by_platform_id_and_contact_information import black_list_check_by_platform_id_or_contact_information


async def black_list_check(
    db: AsyncSession,
    platform_id: str,
    contact_information: str
) -> None:
    blacklist: BlackList | None = await black_list_check_by_platform_id_or_contact_information(
        db,
        platform_id=platform_id,
        contact_information=contact_information    
    )
    
    if blacklist:
        raise ValueError('error.messages.error_validate_vacancy')
    
    