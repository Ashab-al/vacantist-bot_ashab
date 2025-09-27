from aiogram import Bot
from models.user import User
from models.subscription import subscription
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update
from repositories.users.find_users_where_have_subscribe_to_category import find_users_where_have_subscribe_to_category
from models.vacancy import Vacancy
from bot.create_bot import bot
from bot.keyboards.vacancy_keyboard import vacancy_keyboard
from lib.tg.common import jinja_render
from aiogram.exceptions import TelegramForbiddenError
import asyncio
from database import get_async_session_for_bot


BASE_DELAY = 0.1  # минимальная задержка
MAX_DELAY = 1.0   # максимальная задержка

async def send_vacancy_to_users(
    vacancy: Vacancy
):
    async with get_async_session_for_bot() as db:
        users: list[User] = await find_users_where_have_subscribe_to_category(db, vacancy.category_id)
        blocked_user_ids: list[User] = []
        if not users:
            return ValueError("Список пользователей пуст")

        delay: float | int = min(BASE_DELAY + len(users) * 0.002, MAX_DELAY)
        
        for user in users:
            try:
                await send_message(user, vacancy)
            except TelegramForbiddenError:
                blocked_user_ids.append(user.id)
            # TODO except Exceptions
            asyncio.sleep(delay)
        
        if blocked_user_ids:
            await db.execute(
                (
                    update(User)
                    .where(User.id.in_(blocked_user_ids))
                    .values(bot_status=User.BOT_STATUS_BLOCKED)
                )
            )
            await db.commit()



async def send_message(
    user: User,
    vacancy: Vacancy
) -> None:
    hash: dict = { "vacancy": vacancy, "user": user }

    await bot.send_message(
        chat_id=user.platform_id,
        text=await jinja_render('vacancy', hash),
        reply_markup=await vacancy_keyboard(**hash)
    )
