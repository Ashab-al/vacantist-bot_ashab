from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery, ContentType
from lib.tg.common import jinja_render
from sqlalchemy.ext.asyncio import AsyncSession
from database import with_session
from config import i18n, settings
from bot.filters.button import PointsButtonFilter
from services.tg.user.current_user import current_user
from bot.keyboards.with_all_tariffs_keyboard import with_all_tariffs_keyboard
from bot.filters.callback.tariff_callback import TariffCallback
from services.tg.user.update_points import update_points
from services.tg.send_info_about_new_payment import send_info_about_new_payment


router = Router(
    name="Обработчик тарифов и платежей"
)
router.message.filter(
    F.chat.type == "private"
)

@router.message(
    PointsButtonFilter()
)
@with_session
async def reaction_btn_points(
    message: Message,
    session: AsyncSession
) -> None:
    """
    Обрабатывает нажатие кнопки "Поинты" и выводит доступные тарифы пользователю.

    Args:
        message (Message): Объект сообщения от пользователя.
        session (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных.

    Notes:
        - Получает текущего пользователя через `current_user`.
        - Отправляет сообщение с описанием тарифов и клавиатурой для выбора.
    """
    await message.answer(
        await jinja_render(
            'points/description', 
            {
                "user": await current_user(session, message=message)
            }
        ),
        reply_markup=await with_all_tariffs_keyboard()
    )

@router.callback_query(
    F.data == i18n['buttons']['points']
)
@with_session
async def choice_btn_points(
    callback: CallbackQuery, 
    bot: Bot, 
    session: AsyncSession
):
    """
    Обрабатывает нажатие на кнопку "Поинты" через callback_query.

    Args:
        callback (CallbackQuery): Объект callback-запроса.
        bot (Bot): Экземпляр бота Aiogram.
        session (AsyncSession): Асинхронная сессия SQLAlchemy.

    Notes:
        - Отправляет пользователю сообщение с описанием тарифов.
        - Прикрепляет клавиатуру с доступными тарифами.
    """
    await callback.answer()

    await bot.send_message(
        chat_id=callback.from_user.id,
        text=await jinja_render(
            'points/description', 
            {
                "user": await current_user(
                        session, 
                        query=callback
                    )
            }
        ),
        reply_markup=await with_all_tariffs_keyboard()
    )

@router.callback_query(
    TariffCallback.filter()
)
async def reaction_choice_tariff(
    callback: CallbackQuery, 
    callback_data: TariffCallback, 
    bot: Bot
):
    """
    Обрабатывает выбор тарифа пользователем и отправляет инвойс для оплаты.

    Args:
        callback (CallbackQuery): Объект callback-запроса.
        callback_data (TariffCallback): Распакованные данные выбранного тарифа.
        bot (Bot): Экземпляр бота Aiogram.

    Notes:
        - Использует `callback_data` для формирования названия и цены тарифа.
        - Отправляет счет через метод `send_invoice`.
    """
    await callback.answer()
    await bot.send_invoice(
        chat_id=callback.from_user.id,
        title=await jinja_render(
            'payment/title', 
            {"tariff": callback_data.points}
        ),
        description=await jinja_render(
            'points/tariff_callback', 
            {"tariff": callback_data.points}
        ),
        payload=callback_data.pack(),
        currency=callback_data.currency,
        prices=[
            LabeledPrice(
                label=await jinja_render(
                    'points/tariff_callback', 
                    {"tariff": callback_data.points}
                ),
                amount=callback_data.price
            )    
        ]
    )

@router.pre_checkout_query()
@with_session
async def process_pre_checkout_query(
    pre_checkout_query: PreCheckoutQuery, 
    bot: Bot, 
    session: AsyncSession
):
    """
    Обрабатывает pre-checkout запрос от Telegram перед завершением оплаты.

    Args:
        pre_checkout_query (PreCheckoutQuery): Запрос на предоплату.
        bot (Bot): Экземпляр бота Aiogram.
        session (AsyncSession): Асинхронная сессия SQLAlchemy.

    Notes:
        - Обновляет баллы пользователя через `update_points`.
        - В случае ошибки отправляет сообщение об ошибке пользователю и админу.
        - При успешной обработке подтверждает pre-checkout запрос.
    """
    try:
        await update_points(
            session, 
            pre_checkout_query.from_user, 
            TariffCallback.unpack(
                pre_checkout_query.invoice_payload
            ).points
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
        await bot.answer_pre_checkout_query(
            pre_checkout_query.id, 
            ok=True
        )

@router.message(
    F.content_type == ContentType.SUCCESSFUL_PAYMENT
)
async def successful_payment_handler(
    message: Message,
    bot: Bot
):
    """
    Обрабатывает успешную оплату пользователем.

    Args:
        message (Message): Сообщение с информацией об успешной оплате.
        bot (Bot): Экземпляр бота Aiogram.

    Notes:
        - Распаковывает тариф из `invoice_payload`.
        - Отправляет пользователю сообщение о успешной оплате.
        - Уведомляет систему о новом платеже через `send_info_about_new_payment`.
        - Вызывает отображение доступных тарифов через `reaction_btn_points`.
    """
    tariff: TariffCallback = TariffCallback.unpack(
        message.successful_payment.invoice_payload
    )

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