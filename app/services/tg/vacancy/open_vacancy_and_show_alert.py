from aiogram.types import CallbackQuery
from bot.filters.callback.open_vacancy_callback import OpenVacancyCallback
from enums.check_vacancy_enum import CheckVacancyEnum
from lib.tg.common import jinja_render
from models.user import User
from services.tg.user.find_user_by_platform_id import find_user_by_platform_id
from services.tg.vacancy.open_vacancy import open_vacancy
from sqlalchemy.ext.asyncio import AsyncSession


async def open_vacancy_and_show_alert(
    callback: CallbackQuery,
    callback_data: OpenVacancyCallback,
    session: AsyncSession,
) -> tuple[dict, User]:
    """
    Открывает вакансию и показывает предупреждение, если необходимо.
    Args:
        callback (CallbackQuery): Объект колбэка Telegram, вызванного при нажатии кнопки.
        callback_data (OpenVacancyCallback): Данные,
            переданные вместе с callback (в том числе ID вакансии).
        session (AsyncSession): Асинхронная сессия для работы с базой данных.
    Returns:
        tuple (dict, User): Кортеж, содержащий:
            - dict: данные о вакансии и статусе открытия,
            - User: объект пользователя, который запросил вакансию.
    """
    user: User = await find_user_by_platform_id(session, callback.from_user.id)
    vacancy_data: dict = await open_vacancy(session, user, callback_data.vacancy_id)
    alert_data: dict = {}
    if vacancy_data.get("status") == CheckVacancyEnum.WARNING:
        alert_data["text"] = await jinja_render(
            vacancy_data["path_view"], {"open_vacancy": vacancy_data, "user": user}
        )
        alert_data["show_alert"] = True

    await callback.answer(**alert_data)

    return vacancy_data, user
