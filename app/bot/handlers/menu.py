"""Модуль работы с Telegram-ботом через aiogram."""

from aiogram import F, Router
from aiogram.filters.command import Command
from aiogram.types import Message
from bot.filters.button import AdvertisementButtonFilter, HelpButtonFilter
from bot.keyboards.kbs import menu_keyboard
from database import with_session
from lib.tg.common import jinja_render
from services.tg.advertisement import advertisement
from services.tg.user.current_user import current_user
from sqlalchemy.ext.asyncio import AsyncSession

router = Router(name="Обработчик главного меню")
router.message.filter(F.chat.type == "private")


@router.message(Command(commands=['start', 'main_menu']))
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
    await current_user(session, message=message)

    await message.answer(
        (await jinja_render("menu/default"))
        + "\n\n"
        + (await jinja_render("menu/instructions")),
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
