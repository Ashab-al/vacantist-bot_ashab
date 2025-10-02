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
from bot.filters.callback.get_vacancies_callback import GetVacanciesCallback
from services.tg.vacancy.vacancies_for_the_week import fetch_vacancies_for_the_week
from enums.vacancies_for_the_week_enum import VacanciesForTheWeekStatusEnum
import asyncio
from models.vacancy import Vacancy
from models.user import User
from bot.keyboards.vacancy_keyboard import vacancy_keyboard
from bot.keyboards.get_more_vacancies_keyboard import get_more_vacancies_keyboard

DELAY = 0.6

router = Router(name="Обработчик пагинации вакансий")
router.message.filter(F.chat.type == "private")

@router.callback_query(GetVacanciesCallback.filter())
@with_session
async def reaction_get_vacancies(
    callback: CallbackQuery, 
    callback_data: GetVacanciesCallback, 
    session: AsyncSession,
    bot: Bot
):
    user: User = await current_user(session, query=callback)
    vacancies_for_the_week = await fetch_vacancies_for_the_week(
        session,
        user,
        callback_data.page,
        callback_data.page_size
    )
    if vacancies_for_the_week.get('status') != VacanciesForTheWeekStatusEnum.OK:
        await callback.answer(
            text=await jinja_render(f"pagination/{vacancies_for_the_week.get('status').value}"),
            show_alert=True
        )
        return
    
    
    if callback_data.page <= vacancies_for_the_week['meta']['max_pages']:
        next_page = callback_data.page + 1
    

    number: int = await send_vacancies(
        callback,
        vacancies_for_the_week.get('items'),
        callback_data,
        user,
        bot
    )
    await bot.send_message(
        chat_id=callback.from_user.id,
        text=await jinja_render('pagination/sended_vacancies', {"number": number, "count": vacancies_for_the_week['meta']['count']}),
        reply_markup=await get_more_vacancies_keyboard(
            user=user,
            page=next_page
        )
    )
        
async def send_vacancies(
    callback: CallbackQuery, 
    vacancies: list[Vacancy], 
    callback_data: GetVacanciesCallback,
    user: User,
    bot: Bot
) -> int:
    
    number: int = ((callback_data.page - 1) * callback_data.page_size) + 1

    for vacancy in vacancies:
        data: dict[str, object] = {
            "vacancy": vacancy,
            "number": number,
            "user": user
        }

        await bot.send_message(
            chat_id=callback.from_user.id,
            text=await jinja_render('pagination/vacancy', data),
            reply_markup=await vacancy_keyboard(user, vacancy)
        )
        number += 1
        await asyncio.sleep(DELAY)
    
    return number - 1