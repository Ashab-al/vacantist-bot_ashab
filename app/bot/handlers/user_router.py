from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from bot.keyboards.kbs import app_keyboard
from bot.utils.utils import greet_user, get_about_us_text
from lib.tg.common import jinja_render

user_router = Router()
user_router.message.filter(
    F.chat.type.in_({"private"})
)

@user_router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    """
    Обрабатывает команду /start.
    """
    text: str = await jinja_render('menu/default', {"name": "Асхаб"})
    await message.answer(text)


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