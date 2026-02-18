from models import SentMessage, User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def find_sent_messages_by_vacancy_id(
    vacancy_id: int, db: AsyncSession
) -> list[tuple[SentMessage, int]] | None:
    stmt = (
        select(SentMessage, User.platform_id)
        .where(SentMessage.vacancy_id == vacancy_id)
        .join(User, SentMessage.user_id == User.id)
    )

    result = await db.execute(stmt)
    return result.all()
