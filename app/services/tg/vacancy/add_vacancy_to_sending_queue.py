from models.vacancy import Vacancy
import asyncio
from config import vacancy_queue


async def add_vacancy_to_sending_queue(
    vacancy: Vacancy
) -> None:
    print(f"Добавляю вакансию '{vacancy.title}' в очередь на рассылку.")
    await vacancy_queue.put(vacancy)