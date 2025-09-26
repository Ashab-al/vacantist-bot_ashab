from aiogram.types import ReplyKeyboardMarkup, WebAppInfo, InlineKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from lib.tg.common import jinja_render
from bot.filters.callback.tariff_callback import TariffCallback


CURRENCY = 'XTR'
TARIFFS_PRICES = {
    10: 1, 
    30: 85, 
    50: 135, 
    100: 255, 
    150: 362, 
    200: 450
}
MAX_COUNT_BUTTON_IN_LINE = 1

async def with_all_tariffs_keyboard():
    kb = InlineKeyboardBuilder()

    for points, price in TARIFFS_PRICES.items():
        kb.button(
            text= await jinja_render('points/tariff_name', {"tariff": points, "price": price}),
            callback_data=TariffCallback(points=points, price=price, currency=CURRENCY).pack()
        )
    
    kb.adjust(MAX_COUNT_BUTTON_IN_LINE, repeat=True)

    return kb.as_markup()