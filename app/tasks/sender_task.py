import asyncio

from celery import shared_task
from sympy import im

from models.vacancy import Vacancy
from models.user import User
from database import async_session_maker
from query_objects.users.find_users_where_have_subscribe_to_category import (
    find_users_where_have_subscribe_to_category,
)
from services.tg.admin_alert import admin_alert
from bot.create_bot import bot

@shared_task
def sender_task(vacancy: Vacancy) -> None:
    asyncio.run(sender_vacancy(vacancy))


async def sender_vacancy(vacancy: Vacancy) -> None:
    async with async_session_maker() as session:
        users: list[User] = await find_users_where_have_subscribe_to_category(
            session, vacancy.category_id
        )
        if not users:
            await admin_alert(
                bot, f"Для вакансии '{vacancy.title}' не найдено подписчиков."
            )