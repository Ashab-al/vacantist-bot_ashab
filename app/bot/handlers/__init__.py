"""Главный обработчик бота, который объединяет все отдельные роутеры."""

from aiogram import Router
from bot.handlers.block_and_unblock import router as block_and_unblock_router
from bot.handlers.category import router as category_router
from bot.handlers.menu import router as menu_router
from bot.handlers.payment import router as payment_router
from bot.handlers.vacancy import router as vacancy_router
from bot.handlers.vacancy_paginate import router as vacancy_paginate_router
from bot.handlers.spam import router as spam_router

main_router = Router(name="Главный обработчик")

for router in [
    menu_router,
    payment_router,
    block_and_unblock_router,
    category_router,
    vacancy_router,
    vacancy_paginate_router,
    spam_router,
]:
    main_router.include_router(router)
