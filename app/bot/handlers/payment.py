"""Модуль работы с Telegram-ботом через aiogram."""

from aiogram import Bot, F, Router
from aiogram.types import (
    CallbackQuery,
    ContentType,
    LabeledPrice,
    Message,
    PreCheckoutQuery,
)
from bot.filters.button import PointsButtonFilter
from bot.filters.callback.tariff_callback import TariffCallback
from bot.keyboards.with_all_tariffs_keyboard import with_all_tariffs_keyboard
from config import i18n
from database import with_session
from lib.tg.common import jinja_render
from services.tg.point.show_points_info import show_points_info
from services.tg.send_info_about_new_payment import send_info_about_new_payment
from services.tg.user.find_user_by_platform_id import find_user_by_platform_id
from services.tg.user.update_points_for_pre_checkout_query import (
    update_points_for_pre_checkout_query,
)
from sqlalchemy.ext.asyncio import AsyncSession

router = Router(name="Обработчик тарифов и платежей")
router.message.filter(F.chat.type == "private")


@router.message(PointsButtonFilter())
@with_session
async def reaction_btn_points(message: Message, session: AsyncSession) -> None:
    """
    Обрабатывает нажатие кнопки "Поинты" и выводит доступные тарифы пользователю.

    Args:
        message (Message): Объект сообщения от пользователя.
        session (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных.

    Notes:
        - Получает текущего пользователя через `find_user_by_platform_id`.
        - Отправляет сообщение с описанием тарифов и клавиатурой для выбора.
    """
    await show_points_info(message, session)


@router.callback_query(F.data == i18n["buttons"]["points"])
@with_session
async def choice_btn_points(callback: CallbackQuery, bot: Bot, session: AsyncSession):
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
            "points/description",
            {"user": await find_user_by_platform_id(session, callback.from_user.id)},
        ),
        reply_markup=await with_all_tariffs_keyboard(),
    )


@router.callback_query(TariffCallback.filter())
async def reaction_choice_tariff(
    callback: CallbackQuery, callback_data: TariffCallback, bot: Bot
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
        title=await jinja_render("payment/title", {"tariff": callback_data.points}),
        description=await jinja_render(
            "points/tariff_callback", {"tariff": callback_data.points}
        ),
        payload=callback_data.pack(),
        currency=callback_data.currency,
        prices=[
            LabeledPrice(
                label=await jinja_render(
                    "points/tariff_callback", {"tariff": callback_data.points}
                ),
                amount=callback_data.price,
            )
        ],
    )


@router.pre_checkout_query()
@with_session
async def process_pre_checkout_query(
    pre_checkout_query: PreCheckoutQuery, bot: Bot, session: AsyncSession
):
    """
    Обрабатывает pre-checkout запрос от Telegram перед завершением оплаты.

    Args:
        pre_checkout_query (PreCheckoutQuery): Запрос на предоплату.
        bot (Bot): Экземпляр бота Aiogram.
        session (AsyncSession): Асинхронная сессия SQLAlchemy.

    Notes:
        - Обновляет баллы пользователя через `update_points_for_pre_checkout_query`.
        - В случае ошибки отправляет сообщение об ошибке пользователю и админу.
        - При успешной обработке подтверждает pre-checkout запрос.
    """
    await update_points_for_pre_checkout_query(
        pre_checkout_query=pre_checkout_query, bot=bot, session=session
    )
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
@with_session
async def successful_payment_handler(message: Message, session: AsyncSession, bot: Bot):
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

    await send_info_about_new_payment(bot, tariff, message.from_user)
    await message.answer(
        await jinja_render(
            "pre_checkout_query/success_payment", {"points": tariff.points}
        )
    )

    await show_points_info(message=message, session=session)
