from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from lib.tg.common import jinja_render
from sqlalchemy.ext.asyncio import AsyncSession
from database import with_session
from bot.keyboards.with_all_categories_keyboard import with_all_categories_keyboard
from services.tg.category.find_subscribe import find_subscribe
from bot.filters.callback.category_callback import CategoryCallback
from services.tg.user.update_subscription_with_category import update_subscription_with_category
from services.tg.user.current_user import current_user
from bot.filters.callback.open_vacancy_callback import OpenVacancyCallback
from bot.filters.callback.spam_vacancy_callback import SpamVacancyCallback
from services.tg.open_vacancy import open_vacancy
from bot.keyboards.open_vacancy_keyboard import open_vacancy_keyboard
from services.tg.spam_vacancy import spam_vacancy, BLACKLISTED
from enums.check_vacancy_enum import CheckVacancyEnum


router = Router(name="Обработчик вакансий")

@router.callback_query(OpenVacancyCallback.filter())
@with_session
async def reaction_choice_vacancy(
    callback: CallbackQuery, 
    callback_data: OpenVacancyCallback, 
    session: AsyncSession,
    bot: Bot
):
    user = await current_user(session, query=callback)
    vacancy_data: dict = await open_vacancy(session, user, callback_data.vacancy_id)
    alert_data: dict = {}
    if vacancy_data.get('status') == CheckVacancyEnum.WARNING:
        alert_data['text'] = await jinja_render(
            vacancy_data['path_view'], 
            {'open_vacancy': vacancy_data, 'user': user}
        )
        alert_data['show_alert'] = True

    await callback.answer(**alert_data)
    
    if vacancy_data.get('status') == CheckVacancyEnum.OPEN_VACANCY:
        await bot.edit_message_text(
            chat_id=callback.from_user.id,
            message_id=callback.message.message_id,
            text=await jinja_render(
                vacancy_data.get('path_view'), 
                {"open_vacancy": vacancy_data, "user": user}
            ),
            reply_markup=await open_vacancy_keyboard(
                user=user, 
                vacancy=vacancy_data.get('vacancy')
            )
        )

@router.callback_query(SpamVacancyCallback.filter())
@with_session
async def reaction_choice_spam_vacancy(
    callback: CallbackQuery, 
    callback_data: SpamVacancyCallback, 
    session: AsyncSession
):
    await callback.answer(
        await jinja_render(
            'callback_query/spam_vacancy', 
            {
                "outcome": await spam_vacancy(session, callback_data.vacancy_id), 
                "BLACKLISTED": BLACKLISTED
             }
        ),
        show_alert=True
    )