from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery, ContentType
from bot.keyboards.kbs import app_keyboard
from bot.utils.utils import greet_user, get_about_us_text
from lib.tg.common import jinja_render
from sqlalchemy.ext.asyncio import AsyncSession
from database import with_session
from services.tg.user.find_or_create_with_update_by_platform_id import find_or_create_with_update_by_platform_id
from config import i18n, settings
from bot.keyboards.kbs import menu_keyboard
from bot.keyboards.with_all_categories_keyboard import with_all_categories_keyboard
from bot.filters.button import (
    AdvertisementButtonFilter,
    CategoryButtonFilter,
    HelpButtonFilter,
    PointsButtonFilter
)
from services.tg.category.find_subscribe import find_subscribe
from bot.filters.callback.category_callback import CategoryCallback
from services.tg.user.update_subscription_with_category import update_subscription_with_category
from services.tg.user.current_user import current_user
from services.tg.advertisement import advertisement
from bot.keyboards.with_all_tariffs_keyboard import with_all_tariffs_keyboard
from bot.filters.callback.tariff_callback import TariffCallback
from services.tg.user.update_points import update_points
from services.tg.send_info_about_new_payment import send_info_about_new_payment


user_router = Router()
user_router.message.filter(
    F.chat.type.in_({"private"})
)

@user_router.message(CommandStart())
@with_session
async def cmd_start(
    message: Message,
    session: AsyncSession
) -> None:
    """
    Обрабатывает команду /start.
    """
    await current_user(session, message=message)
    
    await message.answer(
        (await jinja_render('menu/default')) 
        + "\n\n" + 
        (await jinja_render('menu/instructions')), 
        reply_markup=await menu_keyboard()
    )

@user_router.message(CategoryButtonFilter())
@with_session
async def reaction_btn_categories(
    message: Message, 
    session: AsyncSession
) -> None:
    subscribed_categories = await find_subscribe(session, message.from_user)
    await message.answer(
        await jinja_render('choice_category'), 
        reply_markup=await with_all_categories_keyboard(session, subscribed_categories)
    )

@user_router.callback_query(CategoryCallback.filter())
@with_session
async def reaction_btn_choice_category(
    query: CallbackQuery, 
    callback_data: CategoryCallback, 
    session: AsyncSession
) -> None:
    """Реакция на кнопки с категориями"""
    view_path: dict[str, str] = await update_subscription_with_category(
        callback_data, 
        session, 
        await find_subscribe(
            session, 
            query.from_user
        ), 
        await current_user(session, query=query)
    )
    await query.message.edit_reply_markup(
        reply_markup=await with_all_categories_keyboard(
            session, 
            await find_subscribe(session, query.from_user)
        )
    )

    await query.answer(
        await jinja_render(f"callback_query/{view_path['path_to_templates']}"),
        show_alert=True
    )

@user_router.message(AdvertisementButtonFilter())
@with_session
async def reaction_btn_advertisement( 
    message: Message,
    session: AsyncSession
) -> None:
    await message.answer(
        await jinja_render(
            'menu/advertisement', 
            {"category_name_and_count": await advertisement(session)}
        )
    )

@user_router.message(HelpButtonFilter())
async def reaction_btn_help(message: Message) -> None:
    await message.answer(await jinja_render('menu/instructions'))

@user_router.message(PointsButtonFilter())
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

@user_router.callback_query(TariffCallback.filter())
async def reaction_choice_tariff(
    query: CallbackQuery, 
    callback_data: TariffCallback, 
    bot: Bot
):
    await query.answer()
    await bot.send_invoice(
        chat_id=query.from_user.id,
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
    

@user_router.pre_checkout_query()
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

    
@user_router.message(
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
