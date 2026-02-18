from aiogram import Bot
from bot.filters.callback.spam_vacancy_callback import (
    IncrementUserBonusForSpamVacancyCallback,
    SpamAndIncrementUserBonusForSpamVacancyCallback,
)
from models import User
from services.tg.spam.notify_the_user_about_the_bonus_transfer import (
    notify_the_user_about_the_bonus_transfer,
)
from services.tg.user.increment_bonus_by_user_platform_id import (
    increment_bonus_by_user_platform_id,
)
from sqlalchemy.ext.asyncio import AsyncSession


async def increment_bonus_and_notify_user(
    callback_data: (
        IncrementUserBonusForSpamVacancyCallback
        | SpamAndIncrementUserBonusForSpamVacancyCallback
    ),
    session: AsyncSession,
    bot: Bot,
) -> User:
    """
    Начисляет бонус пользователю за сообщение о спаме и отправляет ему уведомление.

    Выполняет две операции:
    1. Увеличивает счёт бонусов пользователя в базе данных через сервис `increment_bonus_by_user_platform_id`.
    2. Отправляет пользователю персональное уведомление о начислении бонуса через бота.

    Поддерживает два типа коллбэков — когда бонус начисляется отдельно или как часть обработки спама.

    :param callback_data: Данные коллбэка, содержащие ID пользователя (user_id).
                         Может быть одного из двух типов:
                         - IncrementUserBonusForSpamVacancyCallback
                         - SpamAndIncrementUserBonusForSpamVacancyCallback
    :param session: Асинхронная сессия SQLAlchemy для взаимодействия с базой данных.
    :param bot: Экземпляр Aiogram Bot для отправки уведомления пользователю.
    :return: Объект пользователя (User), которому был начислен бонус.
    """
    user: User = await increment_bonus_by_user_platform_id(
        callback_data.user_id, session
    )
    await notify_the_user_about_the_bonus_transfer(user, bot)

    return user
