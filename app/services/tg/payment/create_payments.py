from asyncio import TaskGroup

from aiogram import Bot
from aiogram.types import CallbackQuery, LabeledPrice
from bot.filters.callback.tariff_callback import TariffCallback
from bot.keyboards.payment_link_button import payment_link_button
from lib.tg.common import jinja_render
from services.tg.user.find_user_by_platform_id import find_user_by_platform_id
from services.tg.yookassa.create_payment import create_payment
from sqlalchemy.ext.asyncio import AsyncSession


async def create_payments(
    callback: CallbackQuery,
    callback_data: TariffCallback,
    bot: Bot,
    session: AsyncSession,
):
    await _send_stars_payment(callback, callback_data, bot)

    await _create_and_send_yookassa_payment(callback, callback_data, session)


async def _send_stars_payment(
    callback: CallbackQuery,
    callback_data: TariffCallback,
    bot: Bot,
) -> None:
    await bot.send_invoice(
        chat_id=callback.from_user.id,
        title=await jinja_render("payment/title", {"tariff": callback_data.points}),
        description=await jinja_render(
            "points/tariff_callback", {"tariff": callback_data.points}
        ),
        payload=callback_data.pack(),
        currency="XTR",
        prices=[
            LabeledPrice(
                label=await jinja_render(
                    "points/tariff_callback", {"tariff": callback_data.points}
                ),
                amount=callback_data.price_xtr,
            )
        ],
    )


async def _create_and_send_yookassa_payment(
    callback: CallbackQuery, callback_data: TariffCallback, session: AsyncSession
) -> None:
    async with TaskGroup() as tg:
        description_task = tg.create_task(
            jinja_render(
                "points/tariff_name",
                {
                    "tariff": callback_data.points,
                    "price_xtr": callback_data.price_xtr,
                    "price_rub": callback_data.price_rub,
                },
            )
        )
        user_task = tg.create_task(
            find_user_by_platform_id(session, callback.from_user.id)
        )
        text_task = tg.create_task(
            jinja_render("payment/card_payment_title", {"tariff": callback_data.points})
        )

    result = create_payment(
        amount=callback_data.price_rub,
        description=description_task.result(),
        user=user_task.result(),
        points_count=callback_data.points,
    )
    await callback.message.answer(
        text=text_task.result(),
        reply_markup=await payment_link_button(result.confirmation.confirmation_url),
    )
