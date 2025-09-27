from aiogram import Router, F
from bot.handlers.menu_router import menu_router
from bot.handlers.payment_router import payment_router
from bot.handlers.block_and_unblock_router import block_and_unblock_router
from bot.handlers.category_router import category_router

main_router = Router(name="Главный обработчик")
main_router.message.filter(F.chat.type == "private")

for router in [
    menu_router, 
    payment_router, 
    block_and_unblock_router,
    category_router
]:
    main_router.include_router(router)