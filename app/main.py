import logging
from contextlib import asynccontextmanager
from bot.create_bot import bot, dp, stop_bot, start_bot
from bot.handlers import main_router
from config import settings
from aiogram.types import Update
from fastapi import FastAPI, Request
from api import api_router


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Starting bot setup...")
    dp.include_router(main_router)

    await start_bot()
    webhook_url = settings.get_webhook_url()
    await bot.set_webhook(
        url=webhook_url,
        allowed_updates=dp.resolve_used_update_types(),
        drop_pending_updates=True
    )

    logging.info(f"Webhook set to {webhook_url}")
    yield
    logging.info("Shutting down bot...")
    await bot.delete_webhook()
    await stop_bot()
    logging.info("Webhook deleted")


app = FastAPI(lifespan=lifespan)

app.include_router(api_router, prefix="/api/v1")

@app.post(
    "/api/v1/webhook", 
    tags=["Telegram API"],
    summary="Эндпоинт для получения обновлений от Telegram",
    description="Телеграм присылает все обновления на этот экшен",
    responses={
        200: {
            "content": {
                "application/json": None
            }
        }
    }
)
async def webhook(
    request: Request
) -> None:
    logging.info("Received webhook request")
    update = Update.model_validate(await request.json(), context={"bot": bot})
    logging.info("ВЕБХУК")
    logging.info(update)
    await dp.feed_update(bot, update)
    logging.info("Update processed")