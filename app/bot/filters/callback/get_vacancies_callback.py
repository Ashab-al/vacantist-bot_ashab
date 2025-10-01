from aiogram.filters.callback_data import CallbackData

class GetVacanciesCallback(CallbackData, prefix="get_vacancies"):
    page: int
    page_size: int