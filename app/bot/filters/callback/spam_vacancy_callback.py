from aiogram.filters.callback_data import CallbackData

class SpamVacancyCallback(CallbackData, prefix="spam_vacancy"):
    """
    Callback-данные для пометки вакансии как спам.

    Attributes:
        vacancy_id (int): Уникальный идентификатор вакансии, которую нужно пометить как спам.

    Этот callback используется для inline-кнопок, чтобы бот мог определить,
    какую именно вакансию пользователь считает спамом и обработать это действие.
    """
    vacancy_id: int
