from aiogram.filters.callback_data import CallbackData


class TariffCallback(CallbackData, prefix="tariff"):
    """
    Callback-данные для выбора тарифа пользователем.

    Attributes:
        points (int): Количество поинтов, предоставляемых выбранным тарифом.
        price (int): Стоимость тарифа.
        currency (str): Валюта, в которой указана цена тарифа.

    Этот callback используется для inline-кнопок, чтобы бот мог определить
    выбранный пользователем тариф и обработать покупку или отображение информации.
    """

    points: int
    price: int
    currency: str
