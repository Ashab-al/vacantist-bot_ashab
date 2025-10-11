from aiogram.filters.callback_data import CallbackData


class CategoryCallback(CallbackData, prefix="category"):
    """
    Callback-данные для inline-кнопок категорий.

    Attributes:
        category_id (int): ID категории, к которой относится действие.

    Этот callback используется для передачи информации о категории при нажатии
    пользователем inline-кнопки. Бот может использовать `category_id`, чтобы
    определить, к какой категории относится действие (подписка или отписка).
    """

    category_id: int
