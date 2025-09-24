from aiogram.filters.callback_data import CallbackData

class TariffCallback(CallbackData, prefix="tariff"):
    tariff: int
    price: int
    currency: str