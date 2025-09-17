from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from bot.keyboards.kbs import app_keyboard
from bot.utils.utils import greet_user, get_about_us_text
from lib.tg.common import jinja_render
from sqlalchemy.ext.asyncio import AsyncSession
from database import with_session
from services.tg.user.find_or_create_with_update_by_platform_id import find_or_create_with_update_by_platform_id
from config import i18n
from bot.keyboards.kbs import menu_keyboard
from bot.filters.button import (
    AdvertisementButtonFilter,
    CategoryButtonFilter,
    HelpButtonFilter,
    PointsButtonFilter
)

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
    await find_or_create_with_update_by_platform_id(
        session,
        message.from_user    
    )
    await message.answer(
        (await jinja_render('menu/default')) 
        + "\n\n" + 
        (await jinja_render('menu/instructions')), 
        reply_markup=await menu_keyboard()
    )

@user_router.message(CategoryButtonFilter())
async def reaction_btn_categories(message: Message) -> None:

    await message.answer("1")

@user_router.message(AdvertisementButtonFilter())
async def reaction_btn_advertisement(message: Message) -> None:

    await message.answer("2")

@user_router.message(HelpButtonFilter())
async def reaction_btn_help(message: Message) -> None:
    await message.answer(await jinja_render('menu/instructions'))

@user_router.message(PointsButtonFilter())
async def reaction_btn_points(message: Message) -> None:

    await message.answer("4")

# @user_router.message(F.text == '🔙 Назад')
# async def cmd_back_home(message: Message) -> None:
#     """
#     Обрабатывает нажатие кнопки "Назад".
#     """
#     await greet_user(message, is_new_user=False)


# @user_router.message(F.text == "ℹ️ О нас")
# async def about_us(message: Message):
#     kb = app_keyboard(user_id=message.from_user.id, first_name=message.from_user.first_name)
#     await message.answer(get_about_us_text(), reply_markup=kb)