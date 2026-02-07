from aiogram import Bot, html
from aiogram.types import CallbackQuery
from bot.filters.callback.spam_vacancy_callback import (
    SpamVacancyCallback,
    IncrementUserBonusForSpamVacancyCallback,
    RejectSpamVacancyCallback,
    SpamVacancyCallbackForAdmin,
    SpamAndIncrementUserBonusForSpamVacancyCallback,
    NotSpamButDeleteMessagesForSpamVacancyCallback,
)
from bot.keyboards.admin_chat_spam_vacancy_button import admin_chat_spam_vacancy_button
from config import i18n, settings
from lib.tg.common import jinja_render
from models.user import User
from models.vacancy import Vacancy
from query_objects.blacklist.black_list_check_by_platform_id_and_contact_information import (
    black_list_check_by_platform_id_or_contact_information,
)
from query_objects.users.get_user_by_platform_id import get_user_by_platform_id
from query_objects.vacancies.find_vacancy_by_id import find_vacancy_by_id
from services.tg.admin_alert import admin_alert_mailing_errors
from sqlalchemy.ext.asyncio import AsyncSession


async def send_spam_vacancy_in_admin_group(
    bot: Bot,
    callback_data: SpamVacancyCallback,
    callback: CallbackQuery,
    session: AsyncSession,
):

    vacancy = await _validate_vacancy(bot, callback_data, session)
    await _validate_blacklist(callback, session)
    user: User = await _validate_user(bot, callback, session)

    await bot.send_message(
        chat_id=settings.admin_chat_id,
        text=await jinja_render(
            "spam/vacancy",
            {
                "username": _username(callback.from_user.username),
                "vacancy": vacancy,
                "user": user,
            },
        ),
        reply_markup=_buttons(callback_data, callback),
        message_thread_id=settings.mailing_new_spam_vacancies_thread_id,
    )
    await callback.answer(
        text=await jinja_render("spam/send_complaint_to_vacancy"), show_alert=True
    )


def _buttons(callback_data: SpamVacancyCallback, callback: CallbackQuery):
    data = {
        "vacancy_id": callback_data.vacancy_id,
        "user_id": callback.from_user.id,
        "message_id": callback.message.message_id,
    }
    args = {
        "spam_vacancy": SpamVacancyCallbackForAdmin,
        "increment_user_bonus_for_spam_vacancy": IncrementUserBonusForSpamVacancyCallback,
        "reject_spam_vacancy": RejectSpamVacancyCallback,
        "spam_and_increment_user_bonus_for_spam_vacancy": SpamAndIncrementUserBonusForSpamVacancyCallback,
        "not_spam_but_delete_messages_for_spam_vacancy": NotSpamButDeleteMessagesForSpamVacancyCallback,
    }
    callback_data_dict = {key: value(**data) for key, value in args.items()}
    return admin_chat_spam_vacancy_button(**callback_data_dict)


def _username(username: str | None) -> str:
    if username is not None:
        return username

    return html.code(i18n["user"]["user_not_has_username"])


async def _validate_vacancy(
    bot: Bot, callback_data: SpamVacancyCallback, session: AsyncSession
):
    vacancy: Vacancy | None = await find_vacancy_by_id(
        session, callback_data.vacancy_id
    )
    if not vacancy:
        await admin_alert_mailing_errors(
            bot,
            f"В send_spam_vacancy_in_admin_group не найдена вакансия ID: {callback_data.vacancy_id}",
        )

        raise ValueError(
            f"В send_spam_vacancy_in_admin_group не найдена вакансия ID: {callback_data.vacancy_id}"
        )

    return vacancy


async def _validate_blacklist(
    callback: CallbackQuery, session: AsyncSession
) -> bool | None:
    if await black_list_check_by_platform_id_or_contact_information(
        session, platform_id=str(callback.from_user.id), contact_information=None
    ):
        await callback.answer(
            text=await jinja_render("callback_query/add_to_blacklist"), show_alert=True
        )
        raise ValueError(f"Вакансия находится в черном списке")


async def _validate_user(
    bot: Bot, callback: CallbackQuery, session: AsyncSession
) -> User:
    user: User | None = await get_user_by_platform_id(session, callback.from_user.id)
    if not user:
        await admin_alert_mailing_errors(
            bot,
            f"В send_spam_vacancy_in_admin_group не найден пользователь с telegram_id: {callback.from_user.id}",
        )

        raise ValueError(
            f"В send_spam_vacancy_in_admin_group не найден пользователь с telegram_id: {callback.from_user.id}"
        )

    return user
