from aiogram.filters.callback_data import CallbackData

class OpenVacancyCallback(CallbackData, prefix="open_vacancy"):
    vacancy_id: int
