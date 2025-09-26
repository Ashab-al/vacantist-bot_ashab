from aiogram.filters.callback_data import CallbackData

class TariffCallback(CallbackData, prefix="tariff"):
    points: int
    price: int
    currency: str