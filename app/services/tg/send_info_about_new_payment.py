from aiogram import Bot
from aiogram.types.user import User as AiogramTgUser
from bot.filters.callback.tariff_callback import TariffCallback
from lib.tg.common import jinja_render
from services.tg.admin_alert import admin_alert_mailing_payments_info


async def send_info_about_new_payment(
    bot: Bot, tariff_data: TariffCallback, aiogram_user: AiogramTgUser
) -> None:
    """
    Отправляет в группу администратора информацию о новом платеже пользователя.

    Args:
        bot (Bot): Экземпляр Telegram-бота для отправки сообщения.
        tariff_data (TariffCallback): Данные о тарифе/платеже.
        aiogram_user (AiogramTgUser): Пользователь Telegram, который совершил платёж.
    """
    await admin_alert_mailing_payments_info(
        bot=bot,
        text=await jinja_render(
            "payment_info_for_admin",
            {
                "name": aiogram_user.first_name,
                "points": tariff_data.points,
                "stars": tariff_data.price,
            },
        ),
    )
