from models.user import User
from models.subscription import subscription
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from enums.bot_status_enum import BotStatusEnum


async def find_users_where_have_subscribe_to_category(
    db: AsyncSession,
    category_id: int
) -> list[User]:
    result = (
        await db.execute(
            select(User)
            .distinct()
            .join(subscription, subscription.c.user_id == User.id)
            .where(subscription.c.category_id == category_id)
            .where(User.bot_status == BotStatusEnum.WORKS)
        )
    ).scalars().all()
    return result
    