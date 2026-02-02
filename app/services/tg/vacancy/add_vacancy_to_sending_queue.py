from config import vacancy_queue
from models.vacancy import Vacancy
import logging

async def add_vacancy_to_sending_queue(vacancy: Vacancy) -> None:
    """
    Добавляет вакансию в очередь на рассылку

    Args:
        vacancy (Vacancy): Объект вакансии, который нужно поставить в очередь
    """
    logging.info(f"Добавляю вакансию '{vacancy.title}' в очередь на рассылку.")
    await vacancy_queue.put(vacancy)
