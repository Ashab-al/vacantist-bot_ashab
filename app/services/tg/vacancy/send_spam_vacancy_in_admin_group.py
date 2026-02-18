from aiogram import Bot, html
from aiogram.types import CallbackQuery
from bot.filters.callback.spam_vacancy_callback import (
    IncrementUserBonusForSpamVacancyCallback,
    NotSpamButDeleteMessagesForSpamVacancyCallback,
    SpamAndIncrementUserBonusForSpamVacancyCallback,
    SpamVacancyCallback,
    SpamVacancyCallbackForAdmin,
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
    """
    Отправляет сообщение о жалобе на спам-вакансию в админ-чат.

    Выполняет следующие действия:
    1. Проверяет существование вакансии.
    2. Проверяет, не находится ли отправитель в чёрном списке.
    3. Находит пользователя в базе данных.
    4. Формирует и отправляет сообщение в админ-чат с кнопками действий.
    5. Подтверждает пользователю, что жалоба отправлена.

    :param bot: Экземпляр Aiogram Bot для отправки сообщений.
    :param callback_data: Данные коллбэка с ID вакансии.
    :param callback: Объект CallbackQuery от пользователя.
    :param session: Асинхронная сессия SQLAlchemy для работы с БД.
    :raises ValueError: Если вакансия или пользователь не найдены, или отправитель в чёрном списке.
    """
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
    """
    Генерирует клавиатуру с действиями для модерации спам-вакансии.

    Создаёт набор callback-данных для четырёх кнопок:
    - Спам (удалить и подтвердить)
    - Начислить бонус
    - Спам + бонус
    - Не спам, но удалить сообщения

    Использует `admin_chat_spam_vacancy_button` для построения инлайн-клавиатуры.

    :param callback_data: Исходные данные коллбэка (ID вакансии).
    :param callback: Объект CallbackQuery для получения контекста (ID сообщения, пользователя).
    :return: Объект InlineKeyboardMarkup с кнопками действий.
    """
    data = {
        "vacancy_id": callback_data.vacancy_id,
        "user_id": callback.from_user.id,
        "message_id": callback.message.message_id,
    }
    args = {
        "spam_vacancy": SpamVacancyCallbackForAdmin,
        "increment_user_bonus_for_spam_vacancy": IncrementUserBonusForSpamVacancyCallback,
        "spam_and_increment_user_bonus_for_spam_vacancy": SpamAndIncrementUserBonusForSpamVacancyCallback,
        "not_spam_but_delete_messages_for_spam_vacancy": NotSpamButDeleteMessagesForSpamVacancyCallback,
    }
    callback_data_dict = {key: value(**data) for key, value in args.items()}
    return admin_chat_spam_vacancy_button(**callback_data_dict)


def _username(username: str | None) -> str:
    """
    Форматирует имя пользователя для отображения.

    Если у пользователя нет username, возвращается кодированный текст-заглушка из локализации.

    :param username: Telegram username пользователя, может быть None.
    :return: Отформатированное имя: либо @username, либо зашифрованное сообщение о его отсутствии.
    """
    if username is not None:
        return username

    return html.code(i18n["user"]["user_not_has_username"])


async def _validate_vacancy(
    bot: Bot, callback_data: SpamVacancyCallback, session: AsyncSession
):
    """
    Проверяет наличие вакансии в базе данных по её ID.

    Если вакансия не найдена — отправляет оповещение администраторам и выбрасывает исключение.

    :param bot: Экземпляр Aiogram Bot для отправки уведомлений об ошибках.
    :param callback_data: Данные коллбэка, содержащие vacancy_id.
    :param session: Асинхронная сессия SQLAlchemy.
    :return: Объект Vacancy, если найден.
    :raises ValueError: Если вакансия не найдена.
    """
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
    """
    Проверяет, находится ли пользователь в чёрном списке по его platform_id.

    Если да — отправляет алерт через callback и выбрасывает исключение.

    :param callback: Объект CallbackQuery, содержит данные пользователя.
    :param session: Асинхронная сессия SQLAlchemy.
    :return: True, если пользователь в чёрном списке (но в этом случае всегда выбрасывается исключение).
    :raises ValueError: Если пользователь или контакт в чёрном списке.
    """
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
    """
    Проверяет наличие пользователя в базе данных по его platform_id (Telegram ID).

    Если пользователь не найден — отправляет оповещение администраторам и выбрасывает исключение.

    :param bot: Экземпляр Aiogram Bot для отправки уведомлений об ошибках.
    :param callback: Объект CallbackQuery, содержит ID пользователя.
    :param session: Асинхронная сессия SQLAlchemy.
    :return: Объект User, если найден.
    :raises ValueError: Если пользователь не найден.
    """
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
