from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from bot.keyboards.kbs import app_keyboard
from bot.utils.utils import greet_user, get_about_us_text
from lib.tg.common import jinja_render
from config import i18n
from fastapi import Depends
from database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from database import with_session

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

    
    await message.answer(await jinja_render('menu/default'))


@user_router.message(F.text == '🔙 Назад')
async def cmd_back_home(message: Message) -> None:
    """
    Обрабатывает нажатие кнопки "Назад".
    """
    await greet_user(message, is_new_user=False)


@user_router.message(F.text == "ℹ️ О нас")
async def about_us(message: Message):
    kb = app_keyboard(user_id=message.from_user.id, first_name=message.from_user.first_name)
    await message.answer(get_about_us_text(), reply_markup=kb)