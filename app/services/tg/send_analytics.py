from bot.create_bot import bot
from enums.bot_status_enum import BotStatusEnum
from lib.tg.common import jinja_render
from models.user import User
from services.tg.admin_alert import admin_alert_mailing_new_users
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession


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
    analytics = dict(result.all())
    analytics["users_count"] = (
        await db.execute(select(func.count()).select_from(User))
    ).scalar()

    await admin_alert_mailing_new_users(
        text=await jinja_render(
            "analytics",
            {"user": user, "analytics": analytics, "bot_status": BotStatusEnum},
        ),
        bot=bot,
    )
