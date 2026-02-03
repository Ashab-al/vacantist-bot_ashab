from sqlalchemy.ext.asyncio import AsyncSession

from models.vacancy import Vacancy

from bot.filters.callback.spam_vacancy_callback import SpamVacancyCallback, SpamVacancyCallbackForAdmin
from aiogram import Bot
from lib.tg.common import jinja_render
from aiogram.types import CallbackQuery
from bot.keyboards.admin_chat_spam_vacancy_button import admin_chat_spam_vacancy_button
from config import settings
from query_objects.vacancies.find_vacancy_by_id import find_vacancy_by_id
from services.tg.admin_alert import admin_alert_mailing_errors


async def send_spam_vacancy_in_admin_group(
    bot: Bot,
    callback_data: SpamVacancyCallback,
    callback: CallbackQuery,
    session: AsyncSession
):
    # TODO: Обработка если пользователь уже нажимал на спам

    spam_vacancy: SpamVacancyCallbackForAdmin = SpamVacancyCallbackForAdmin(
        vacancy_id=callback_data.vacancy_id,
        user_id=callback.from_user.id,
        message_id=callback.message.message_id
    )

    vacancy: Vacancy | None = await find_vacancy_by_id(session, callback_data.vacancy_id)
    if not vacancy:
        await admin_alert_mailing_errors(
            bot,
            f"В send_spam_vacancy_in_admin_group не найдена вакансия ID: {callback_data.vacancy_id}"
        )

        raise ValueError(f"В send_spam_vacancy_in_admin_group не найдена вакансия ID: {callback_data.vacancy_id}")

    btn = await admin_chat_spam_vacancy_button(spam_vacancy)
    text = f"""
        Пользователь @{callback.from_user.username} пометил вакансию как спам.
        Вакансия ID: {callback_data.vacancy_id}
    """
    text += "\n----------------------\n" + vacancy.description

    await bot.send_message(
        chat_id=settings.admin_chat_id,
        text=text,
        reply_markup=btn,
        message_thread_id=settings.mailing_new_spam_vacancies_thread_id
    )