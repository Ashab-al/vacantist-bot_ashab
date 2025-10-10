from models.user import User
from models.subscription import subscription
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from enums.bot_status_enum import BotStatusEnum


async def find_users_where_have_subscribe_to_category(
    db: AsyncSession, category_id: int
) -> list[User]:
    """
    Найти пользователей, которые подписаны на указанную категорию и находятся в статусе `WORKS`.

    Args:
        db (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных.
        category_id (int): ID категории, по которой ищутся подписанные пользователи.

    Returns:
        list[User]: Список пользователей, подписанных на категорию и активных в системе.
    """
    result = (
        (
            await db.execute(
                select(User)
                .distinct()
                .join(subscription, subscription.c.user_id == User.id)
                .where(subscription.c.category_id == category_id)
                .where(User.bot_status == BotStatusEnum.WORKS)
            )
        )
        .scalars()
        .all()
    )
    return result
