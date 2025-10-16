from aiogram.types import Message
from bot.keyboards.with_all_tariffs_keyboard import with_all_tariffs_keyboard
from lib.tg.common import jinja_render
from services.tg.user.find_user_by_platform_id import find_user_by_platform_id
from sqlalchemy.ext.asyncio import AsyncSession


async def show_points_info(message: Message, session: AsyncSession):
    """
    Обрабатывает нажатие кнопки "Поинты" в Telegram-боте.

    Функция:
    - Получает текущего пользователя из базы данных с помощью `find_user_by_platform_id`.
    - Формирует сообщение с описанием очков пользователя через шаблон Jinja2 (`points/description`).
    - Отправляет сообщение пользователю с клавиатурой, содержащей все доступные тарифы.

    Args:
        message (Message): Объект входящего сообщения Telegram.
        session (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных.
    """
    await message.answer(
        await jinja_render(
            "points/description",
            {"user": await find_user_by_platform_id(session, message.from_user.id)},
        ),
        reply_markup=await with_all_tariffs_keyboard(),
    )
