"""Модуль работы с Telegram-ботом через aiogram."""

from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from bot.filters.button import CategoryButtonFilter
from bot.filters.callback.category_callback import CategoryCallback
from bot.keyboards.with_all_categories_keyboard import with_all_categories_keyboard
from database import with_session
from lib.tg.common import jinja_render
from services.tg.category.find_subscribe import find_subscribe
from services.tg.user.find_user_by_platform_id import find_user_by_platform_id
from services.tg.user.update_subscription_with_category import (
    update_subscription_with_category,
)
from sqlalchemy.ext.asyncio import AsyncSession

router = Router(name="Обработчик категорий")
router.message.filter(F.chat.type == "private")


@router.message(CategoryButtonFilter())
@with_session
async def reaction_btn_categories(message: Message, session: AsyncSession) -> None:
    """
    Обрабатывает нажатие на кнопку категорий в главном меню.

    Args:
        message (Message): Объект сообщения от пользователя.
        session (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных.

    Notes:
        - Получает список категорий в виде inline кнопок.
        - Отправляет сообщение с клавиатурой,
        где пользователь может выбрать или изменить подписки на категории.
    """
    subscribed_categories = await find_subscribe(session, message.from_user)
    await message.answer(
        await jinja_render("choice_category"),
        reply_markup=await with_all_categories_keyboard(session, subscribed_categories),
    )


@router.callback_query(CategoryCallback.filter())
@with_session
async def reaction_btn_choice_category(
    query: CallbackQuery, callback_data: CategoryCallback, session: AsyncSession
) -> None:
    """
    Обрабатывает нажатие на inline-кнопки категорий.

    Args:
        query (CallbackQuery): CallbackQuery от пользователя.
        callback_data (CategoryCallback): Данные callback для выбранной категории.
        session (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных.

    Notes:
        - Обновляет подписку пользователя на выбранную категорию
        через `update_subscription_with_category`.
        - Обновляет клавиатуру сообщений с категориями.
        - Отправляет пользователю уведомление (show_alert) с результатом действия.
    """

    view_path: dict[str, str] = await update_subscription_with_category(
        callback_data,
        session,
        await find_subscribe(session, query.from_user),
        await find_user_by_platform_id(session, query.from_user.id),
    )
    await query.message.edit_reply_markup(
        reply_markup=await with_all_categories_keyboard(
            session, await find_subscribe(session, query.from_user)
        )
    )

    await query.answer(
        await jinja_render(f"callback_query/{view_path['path_to_templates']}"),
        show_alert=True,
    )
