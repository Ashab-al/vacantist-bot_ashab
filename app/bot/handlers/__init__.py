"""Модуль работы с Telegram-ботом через aiogram."""

from aiogram import F, Router
from bot.handlers.block_and_unblock import router as block_and_unblock_router
from bot.handlers.category import router as category_router
from bot.handlers.menu import router as menu_router
from bot.handlers.payment import router as payment_router
from bot.handlers.vacancy import router as vacancy_router
from bot.handlers.vacancy_paginate import router as vacancy_paginate_router

main_router = Router(name="Главный обработчик")
main_router.message.filter(F.chat.type == "private")

for router in [
    menu_router,
    payment_router,
    block_and_unblock_router,
    category_router,
    vacancy_router,
    vacancy_paginate_router,
]:
    main_router.include_router(router)
