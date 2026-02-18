from asyncio import TaskGroup

from aiogram import Bot
from aiogram.types import CallbackQuery
from bot.filters.callback.spam_vacancy_callback import (
    SpamAndIncrementUserBonusForSpamVacancyCallback,
)
from lib.tg.common import jinja_render
from models import User
from services.tg.spam.add_vacancy_to_blacklist import add_vacancy_to_blacklist
from services.tg.spam.delete_all_messages_with_vacancy_from_users import (
    delete_all_messages_with_vacancy_from_users,
)
from services.tg.spam.increment_user_bonus import increment_bonus_and_notify_user
from database import with_session


async def add_to_spam_and_increment_user_bonus_then_update_message(
    callback: CallbackQuery,
    callback_data: SpamAndIncrementUserBonusForSpamVacancyCallback,
    bot: Bot,
) -> None:
    """
    Обрабатывает нажатие кнопки "Спам + бонус" в админ-группе.

    Запускает три задачи параллельно:
    - удаление всех сообщений с вакансией у пользователей,
    - добавление вакансии в чёрный список,
    - начисление бонуса пользователю.

    После завершения — обновляет текст сообщения в админ-чате.

    :param callback: Объект CallbackQuery от Telegram.
    :param callback_data: Данные коллбэка, содержащие ID вакансии и пользователя.
    :param bot: Экземпляр бота Aiogram для отправки уведомлений.
    """
    async with TaskGroup() as tg:
        tg.create_task(
            _delete_all_messages_with_vacancy_from_users(callback_data)
        )
        tg.create_task(_add_vacancy_to_blacklist(callback, callback_data))
        user_task = tg.create_task(
            _increment_bonus_and_notify_user(callback_data, bot)
        )

    await callback.message.edit_text(
        text=await _generate_text(callback, user_task.result()),
        reply_markup=callback.message.reply_markup,
    )


@with_session
async def _increment_bonus_and_notify_user(
    callback_data: SpamAndIncrementUserBonusForSpamVacancyCallback,
    bot: Bot,
    **kwargs
):
    """
    Начисляет бонус пользователю за сообщение о спаме и уведомляет его через бота.

    Использует внешний сервис increment_bonus_and_notify_user.
    Выполняется в рамках сессии базы данных.

    :param callback_data: Данные коллбэка с информацией о пользователе и вакансии.
    :param bot: Экземпляр бота для отправки уведомления пользователю.
    :param kwargs: Дополнительные аргументы, включая сессию БД.
    :return: Объект пользователя после начисления бонуса.
    """
    return await increment_bonus_and_notify_user(callback_data, kwargs["session"], bot)

@with_session
async def _delete_all_messages_with_vacancy_from_users(
    callback_data: SpamAndIncrementUserBonusForSpamVacancyCallback,
    **kwargs
):
    """
    Удаляет все сообщения с указанной вакансией из переписок пользователей.

    Выполняется в рамках сессии базы данных.
    Удаление происходит асинхронно через соответствующий сервис.

    :param callback_data: Данные коллбэка с ID вакансии.
    :param kwargs: Дополнительные аргументы, включая сессию БД.
    """
    await delete_all_messages_with_vacancy_from_users(
        callback_data, kwargs["session"]
    )

@with_session
async def _add_vacancy_to_blacklist(
    callback: CallbackQuery,
    callback_data: SpamAndIncrementUserBonusForSpamVacancyCallback,
    **kwargs
):
    """
    Добавляет вакансию в чёрный список (базу спама).

    Если вакансия уже в списке, выбрасывается ValueError.
    Ошибка обрабатывается и отправляется ответ в чат.

    :param callback: Объект CallbackQuery для отправки сообщения об ошибке.
    :param callback_data: Данные с ID вакансии.
    :param kwargs: Дополнительные аргументы, включая сессию БД.
    """
    try:
        await add_vacancy_to_blacklist(
            callback_data.vacancy_id,
            kwargs["session"]
        )
    except ValueError as e:
        await callback.message.answer(f"Ошибка: {e}")

async def _generate_text(
    callback: CallbackQuery,
    user: User
) -> str:
    """
    Генерирует финальный текст сообщения после обработки спама.

    Применяет цепочку шаблонов Jinja2:
    1. Добавляет информацию о начислении бонуса пользователю.
    2. Обновляет статус сообщения в админ-группе.
    3. Указывает, что все спам-сообщения удалены.

    :param callback: Объект CallbackQuery для доступа к исходному тексту.
    :param user: Пользователь, которому был начислен бонус.
    :return: Итоговый текст для редактирования сообщения.
    """
    text: str = await jinja_render(
        "spam/increment_user_bonus", {"text": callback.message.text, "user": user}
    )
    text = await jinja_render("spam/update_spam_message_in_admin_group", {"text": text})
    text = await jinja_render("spam/update_spam_message_delete_all_spam_messages", {"text": text})
    return text
