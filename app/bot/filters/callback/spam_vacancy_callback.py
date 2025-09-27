from aiogram.filters.callback_data import CallbackData

class SpamVacancyCallback(CallbackData, prefix="spam_vacancy"):
    vacancy_id: int
