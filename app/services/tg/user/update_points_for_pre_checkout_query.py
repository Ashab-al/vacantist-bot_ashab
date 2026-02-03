from aiogram import Bot
from aiogram.types import PreCheckoutQuery
from bot.filters.callback.tariff_callback import TariffCallback
from lib.tg.common import jinja_render
from services.tg.admin_alert import admin_alert_mailing_errors
from services.tg.user.update_points import update_points
from sqlalchemy.ext.asyncio import AsyncSession


async def update_points_for_pre_checkout_query(
    pre_checkout_query: PreCheckoutQuery, bot: Bot, session: AsyncSession
) -> None:
    """
    Обновляет поинты пользователя через `update_points`.

    Если все прошло успешно, возвращает None.
    В случае ошибки отправляет сообщение об ошибке пользователю и администратору
    и пробрасывает эту ошибку дальше.

    Args:
        pre_checkout_query (PreCheckoutQuery): Объект PreCheckoutQuery от Telegram.
        bot (Bot): Экземпляр бота Aiogram.
        session (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных.

    Raises:
        Exception: Пробрасывает исключение, если ошибка не обработана.
    """
    try:
        await update_points(
            session,
            pre_checkout_query.from_user,
            TariffCallback.unpack(pre_checkout_query.invoice_payload).points,
        )
    except Exception as e:  # pylint: disable=broad-except
        await bot.send_message(
            chat_id=pre_checkout_query.from_user.id,
            text=await jinja_render("pre_checkout_query/fail_payment"),
        )

        await admin_alert_mailing_errors(
            bot=bot,
            text="\n\n".join([str(e), "Метод process_pre_checkout_query"]),
        )
        raise e from e

    return None
