"""Обработчики команд главного меню бота."""

from aiogram import F, Router
from aiogram.filters.command import Command
from aiogram.types import Message
from bot.filters.button import AdvertisementButtonFilter, HelpButtonFilter
from bot.keyboards.kbs import menu_keyboard
from database import with_session
from enums.bot_status_enum import BotStatusEnum
from exceptions.user_not_found_error import UserNotFoundError
from lib.tg.common import jinja_render
from models.user import User
from services.tg.advertisement import advertisement
from services.tg.send_analytics import send_analytics
from services.tg.user.create_user import create_user
from services.tg.user.find_user_by_platform_id import find_user_by_platform_id
from services.tg.user.update_bot_status import update_bot_status
from sqlalchemy.ext.asyncio import AsyncSession


router = Router(name="Обработчик главного меню")
router.message.filter(F.chat.type == "private")


@router.message(Command(commands=["start", "main_menu"]))
@with_session
async def cmd_start(message: Message, session: AsyncSession) -> None:
    """
    Обрабатывает команду /start.

    Args:
        message (Message): Объект сообщения от пользователя.
        session (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных.

    Notes:
        - Создает или обновляет пользователя через `current_user`.
        - Отправляет приветственное сообщение с инструкциями.
        - Прикрепляет основное меню с кнопками.
    """
    try:
        user: User = await find_user_by_platform_id(session, message.from_user.id)
        if user.bot_status == BotStatusEnum.BOT_BLOCKED:
            user = await update_bot_status(session, user, BotStatusEnum.WORKS)
    except UserNotFoundError:
        user = await create_user(session, message.from_user)
        await send_analytics(session, user)

    await message.answer(
        "\n\n".join(
            [
                await jinja_render("menu/default"),
                await jinja_render("menu/instructions"),
            ]
        ),
        reply_markup=await menu_keyboard(),
    )


@router.message(AdvertisementButtonFilter())
@with_session
async def reaction_btn_advertisement(message: Message, session: AsyncSession) -> None:
    """
    Обрабатывает нажатие на кнопку "Реклама" в главном меню.

    Args:
        message (Message): Объект сообщения от пользователя.
        session (AsyncSession): Асинхронная сессия SQLAlchemy для работы с базой данных.

    Notes:
        - Получает список категорий с количеством
        подписчиков на эти категории через `advertisement`.
    """
    await message.answer(
        await jinja_render(
            "menu/advertisement",
            {"category_name_and_count": await advertisement(session)},
        )
    )


@router.message(HelpButtonFilter())
async def reaction_btn_help(message: Message) -> None:
    """
    Обрабатывает нажатие на кнопку "Помощь" в главном меню.

    Args:
        message (Message): Объект сообщения от пользователя.

    Notes:
        - Отправляет пользователю инструкцию по использованию бота.
    """
    await message.answer(await jinja_render("menu/instructions"))
