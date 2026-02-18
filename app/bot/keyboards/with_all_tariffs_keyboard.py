from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup
from bot.filters.callback.tariff_callback import TariffCallback
from lib.tg.common import jinja_render

CURRENCY_XTR = "XTR"
CURRENCY_RUB = "RUB"

TARIFFS_PRICES = {
    10: {CURRENCY_XTR: 50, CURRENCY_RUB: 90},  # 5.0 звезд за штуку
    20: {CURRENCY_XTR: 90, CURRENCY_RUB: 160},  # 4.5 звезд за штуку
    30: {CURRENCY_XTR: 135, CURRENCY_RUB: 240},  # 4.5 звезд за штуку
    50: {CURRENCY_XTR: 135, CURRENCY_RUB: 390},  # 4.4 звезд за штуку
    100: {CURRENCY_XTR: 400, CURRENCY_RUB: 712},  # 4.0 звезд за штуку
    150: {CURRENCY_XTR: 550, CURRENCY_RUB: 979},  # 3.7 звезд за штуку
    200: {CURRENCY_XTR: 700, CURRENCY_RUB: 1246},  # 3.5 звезд за штуку
}

MAX_COUNT_BUTTON_IN_LINE = 1
EMOJI_ID = "5471952986970267163"
BUTTON_STYLE = "primary"


async def with_all_tariffs_keyboard() -> InlineKeyboardMarkup:
    """
    Создать и вернуть клавиатуру с тарифами.

    Для каждого тарифа формируется кнопка с количеством поинтов и ценой.
    Данные берутся из словаря `TARIFFS_PRICES`.

    Returns:
        InlineKeyboardMarkup: Объект клавиатуры с кнопками всех доступных тарифов.
    """
    kb = InlineKeyboardBuilder()

    for points, currencies in TARIFFS_PRICES.items():
        kb.button(
            text=await jinja_render(
                "points/tariff_name",
                {
                    "tariff": points,
                    "price_xtr": currencies[CURRENCY_XTR],
                    "price_rub": currencies[CURRENCY_RUB],
                },
            ),
            callback_data=TariffCallback(
                points=points,
                price_xtr=currencies[CURRENCY_XTR],
                price_rub=currencies[CURRENCY_RUB],
            ).pack(),
            style=BUTTON_STYLE,
            icon_custom_emoji_id=EMOJI_ID,
        )

    kb.adjust(MAX_COUNT_BUTTON_IN_LINE, repeat=True)

    return kb.as_markup()
