from models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from enums.bot_status_enum import BotStatusEnum
from config import settings
from lib.tg.common import jinja_render
from bot.create_bot import bot


async def send_analytics(db: AsyncSession, user: User) -> None:
    """
    Отправляет в группу администратора информацию о новом пользователе и также
    статистику всех пользователей.

    Args:
        db (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных.
        user (User): Объект пользователя.
    """
    result = await db.execute(
        select(User.bot_status, func.count()).group_by(User.bot_status)
    )
    analytics = {status: count for status, count in result.all()}
    analytics["users_count"] = (
        await db.execute(select(func.count()).select_from(User))
    ).scalar()

    await bot.send_message(
        chat_id=settings.admin_chat_id,
        text=await jinja_render(
            "analytics",
            {"user": user, "analytics": analytics, "bot_status": BotStatusEnum},
        ),
    )
