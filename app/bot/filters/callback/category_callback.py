from aiogram.filters.callback_data import CallbackData


class CategoryCallback(CallbackData, prefix="category"):
    """
    Callback-данные для inline-кнопок категорий.

    Используется для передачи `category_id` при нажатии на кнопку,
    чтобы бот мог определить, к какой категории относится действие
    (подписка или отписка).
    """
    category_id: int
