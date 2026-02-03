from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup
from bot.filters.callback.tariff_callback import TariffCallback
from lib.tg.common import jinja_render

CURRENCY = "XTR"
TARIFFS_PRICES = {
    10: 50,  # 5.0 звезд за штуку
    20: 90,  # 4.5 звезд за штуку
    30: 135,  # 4.5 звезд за штуку
    50: 220,  # 4.4 звезд за штуку
    100: 400,  # 4.0 звезд за штуку
    150: 550,  # 3.7 звезд за штуку
    200: 700,  # 3.5 звезд за штуку
}
MAX_COUNT_BUTTON_IN_LINE = 1


async def with_all_tariffs_keyboard() -> InlineKeyboardMarkup:
    """
    Создать и вернуть клавиатуру с тарифами.

    Для каждого тарифа формируется кнопка с количеством поинтов и ценой.
    Данные берутся из словаря `TARIFFS_PRICES`.

    Returns:
        InlineKeyboardMarkup: Объект клавиатуры с кнопками всех доступных тарифов.
    """
    kb = InlineKeyboardBuilder()

    for points, price in TARIFFS_PRICES.items():
        kb.button(
            text=await jinja_render(
                "points/tariff_name", {"tariff": points, "price": price}
            ),
            callback_data=TariffCallback(
                points=points, price=price, currency=CURRENCY
            ).pack(),
        )

    kb.adjust(MAX_COUNT_BUTTON_IN_LINE, repeat=True)

    return kb.as_markup()
