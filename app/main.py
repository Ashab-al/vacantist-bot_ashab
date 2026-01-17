"""
Главный файл запуска FastAPI-приложения с интеграцией Telegram-бота.

- Настройка webhook Telegram
- Запуск и остановка бота
- Подключение API и обработчиков
- Управление жизненным циклом приложения через lifespan
"""

# pylint: disable=broad-except, unused-import
import asyncio  # noqa: F401
import logging
from contextlib import asynccontextmanager

from aiogram.types import Update
from api import api_router
from bot.create_bot import bot, dp, start_bot, stop_bot
from bot.handlers import main_router
from config import settings, vacancy_queue  # noqa: F401
from enums.mode_enum import ModeEnum
from fastapi import FastAPI, Request
from services.tg.vacancy.sender_worker import sender_worker  # noqa: F401

# pylint: enable=broad-except, unused-import
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """
    Управляет жизненным циклом приложения FastAPI с Telegram-ботом.

    Подключает маршруты бота, устанавливает webhook, запускает воркер отправки
    вакансий (TODO), и корректно завершает работу бота при остановке приложения.

    Args:
        app (FastAPI): Экземпляр FastAPI приложения.
    """
    logging.info("Starting bot setup...")
    dp.include_router(main_router)

    await start_bot()
    webhook_url = settings.get_webhook_url()

    drop_pending_updates: bool | None = None
    if settings.mode == ModeEnum.PRODUCTION:
        drop_pending_updates = False
    elif settings.mode == ModeEnum.DEVELOP:
        drop_pending_updates = True
    try:
        logging.info(f"Webhook set to {webhook_url}")
        await bot.set_webhook(
            url=webhook_url,
            allowed_updates=dp.resolve_used_update_types(),
            drop_pending_updates=drop_pending_updates,
        )
    except Exception as e:
        logging.error(f"!!! Webhook NOT set: {e}")
        logging.info("Application will continue to work without webhook for now.")

    worker_task = asyncio.create_task(sender_worker(vacancy_queue, bot))

    logging.info("Webhook set to %s", webhook_url)

    yield

    logging.info("Sending shutdown signal to sender_worker...")
    # await vacancy_queue.put(None)#TODO потом включить # pylint: disable=fixme
    # await vacancy_queue.join()#TODO потом включить # pylint: disable=fixme
    worker_task.cancel()  # TODO потом включить # pylint: disable=fixme
    logging.info("Sender_worker finished successfully.")

    logging.info("Shutting down bot...")
    await bot.delete_webhook()

    await stop_bot()
    logging.info("Webhook deleted")


common_kwargs: dict = {
    "lifespan": lifespan,
    "title": "Vacantist Bot",
    "description": "Telegram-бот для поиска вакансий",
}

if settings.mode == ModeEnum.PRODUCTION:
    common_kwargs.update(docs_url=None, redoc_url=None, openapi_url=None)

app = FastAPI(**common_kwargs)
app.include_router(api_router, prefix="/api/v1")


@app.post(
    "/api/v1/webhook",
    tags=["Telegram API"],
    summary="Эндпоинт для получения обновлений от Telegram",
    description="Телеграм присылает все обновления на этот экшен",
    responses={200: {"content": {"application/json": None}}},
)
async def webhook(request: Request) -> None:
    """
    Обрабатывает входящие обновления от Telegram через webhook.

    Args:
        request (Request): Объект запроса FastAPI с данными Telegram.

    Raises:
        HTTPException: Если происходит ошибка при обработке обновления.

    Notes:
        Обновление валидируется и передается в диспетчер dp.feed_update для обработки.
    """
    await dp.feed_update(
        bot, Update.model_validate(await request.json(), context={"bot": bot})
    )
