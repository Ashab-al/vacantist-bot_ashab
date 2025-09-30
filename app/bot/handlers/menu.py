from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters.command import CommandStart

from lib.tg.common import jinja_render
from sqlalchemy.ext.asyncio import AsyncSession
from database import with_session
from bot.keyboards.kbs import menu_keyboard
from bot.filters.button import (
    AdvertisementButtonFilter,
    HelpButtonFilter,
)

from services.tg.user.current_user import current_user
from services.tg.advertisement import advertisement


router = Router(name="Обработчик главного меню")
router.message.filter(F.chat.type == "private")

@router.message(CommandStart())
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


@router.message(AdvertisementButtonFilter())
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

@router.message(HelpButtonFilter())
async def reaction_btn_help(message: Message) -> None:
    await message.answer(await jinja_render('menu/instructions'))


