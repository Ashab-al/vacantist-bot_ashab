from aiogram import Bot
from models.user import User
from sqlalchemy import update
from repositories.users.find_users_where_have_subscribe_to_category import find_users_where_have_subscribe_to_category
from models.vacancy import Vacancy
from bot.keyboards.vacancy_keyboard import vacancy_keyboard
from lib.tg.common import jinja_render
from aiogram.exceptions import TelegramForbiddenError
import asyncio
from database import get_async_session_for_bot


BASE_DELAY = 0.1  # минимальная задержка
MAX_DELAY = 1.0   # максимальная задержка
DELAY = 0.4
async def sender_worker(
    queue: asyncio.Queue,
    bot: Bot
):
    print("Воркер для рассылки запущен и ждет вакансии...")
    while True:
        print("ЦИКЛ ЗАПУЩЕН, ОЖИДАЮ ВАКАНСИИ")
        vacancy: Vacancy | None = await queue.get()
        
        if vacancy is None:
            print("Получен сигнал на завершение. Воркер останавливается.")
            queue.task_done()
            break
        print(f"Начинаю рассылку вакансии: {vacancy.title}")

        async with get_async_session_for_bot() as db:
            users: list[User] = await find_users_where_have_subscribe_to_category(db, vacancy.category_id)
            blocked_user_ids: list[int] = []
            if not users:
                print(f"Для вакансии '{vacancy.title}' не найдено подписчиков.")
                
                queue.task_done()
                continue 

            delay: float | int = DELAY
            
            for user in users:
                try:
                    res = await bot.send_message(
                        chat_id=user.platform_id,
                        text=await jinja_render('vacancy', { "vacancy": vacancy, "user": user }),
                        reply_markup=await vacancy_keyboard(vacancy=vacancy, user=user)
                    )
                    print("ВАКАНСИЯ ОТПРАВЛЕНА")
                    print(res)
                except TelegramForbiddenError:
                    blocked_user_ids.append(user.id)
                # TODO except Exceptions
                await asyncio.sleep(delay)
            
            if blocked_user_ids:
                await db.execute(
                    (
                        update(User)
                        .where(User.id.in_(blocked_user_ids))
                        .values(bot_status=User.BOT_STATUS_BLOCKED)
                    )
                )
                await db.commit()
                print(f"Обновлен статус для {len(blocked_user_ids)} заблокированных пользователей.")

        queue.task_done()
        print(f"Рассылка вакансии '{vacancy.title}' завершена.")
    
    print("ВЫХОД ИЗ ЦИКЛА")