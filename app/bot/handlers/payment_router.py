from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery, ContentType
from lib.tg.common import jinja_render
from sqlalchemy.ext.asyncio import AsyncSession
from database import with_session
from config import i18n, settings
from bot.filters.button import (
    PointsButtonFilter
)
from services.tg.user.current_user import current_user
from bot.keyboards.with_all_tariffs_keyboard import with_all_tariffs_keyboard
from bot.filters.callback.tariff_callback import TariffCallback
from services.tg.user.update_points import update_points
from services.tg.send_info_about_new_payment import send_info_about_new_payment
from bot.handlers import payment_router

payment_router = Router(name="Обработчик тарифов и платежей")
payment_router.message.filter(F.chat.type == "private")

@payment_router.message(PointsButtonFilter())
@with_session
async def reaction_btn_points(
    message: Message,
    session: AsyncSession
) -> None:
    """Вывод тарифов"""
    await message.answer(
        await jinja_render(
            'points/description', 
            {"user": await current_user(session, message=message)}
        ),
        reply_markup=await with_all_tariffs_keyboard()
    )

@payment_router.callback_query(F.data == i18n['buttons']['points'])
@with_session
async def choice_btn_points(
    callback: CallbackQuery, 
    bot: Bot, 
    session: AsyncSession
):
    await callback.answer()

    await bot.send_message(
        chat_id=callback.from_user.id,
        text=await jinja_render(
            'points/description', 
            {"user": await current_user(session, query=callback)}
        ),
        reply_markup=await with_all_tariffs_keyboard()
    )

@payment_router.callback_query(TariffCallback.filter())
async def reaction_choice_tariff(
    callback: CallbackQuery, 
    callback_data: TariffCallback, 
    bot: Bot
):
    await callback.answer()
    await bot.send_invoice(
        chat_id=callback.from_user.id,
        title=await jinja_render('payment/title', {"tariff": callback_data.points}),
        description=await jinja_render('points/tariff_callback', {"tariff": callback_data.points}),
        payload=callback_data.pack(),
        currency=callback_data.currency,
        prices=[
            LabeledPrice(
                label=await jinja_render('points/tariff_callback', {"tariff": callback_data.points}),
                amount=callback_data.price
            )    
        ]
    )

@payment_router.pre_checkout_query()
@with_session
async def process_pre_checkout_query(
    pre_checkout_query: PreCheckoutQuery, 
    bot: Bot, 
    session: AsyncSession
):
    try:
        await update_points(
            session, 
            pre_checkout_query.from_user, 
            TariffCallback.unpack(pre_checkout_query.invoice_payload).points
        )
    except Exception as e:
        await bot.send_message(
            chat_id=pre_checkout_query.from_user.id,
            text=await jinja_render('pre_checkout_query/fail_payment')
        )
        
        await bot.send_message(
            chat_id=settings.admin_chat_id,
            text=str(e) + "\n\nМетод process_pre_checkout_query"
        )
    else:
        await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

    
@payment_router.message(
    F.content_type == ContentType.SUCCESSFUL_PAYMENT
)
async def successful_payment_handler(
    message: Message,
    bot: Bot
):
    tariff: TariffCallback = TariffCallback.unpack(message.successful_payment.invoice_payload)

    await send_info_about_new_payment(
        bot,
        tariff,
        message.from_user
    )
    await message.answer(
        await jinja_render(
            'pre_checkout_query/success_payment', 
            {
                "points": tariff.points
            }
        )
    )

    await reaction_btn_points(message=message)