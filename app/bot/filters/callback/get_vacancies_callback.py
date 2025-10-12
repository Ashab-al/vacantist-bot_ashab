from aiogram.filters.callback_data import CallbackData


class GetVacanciesCallback(CallbackData, prefix="get_vacancies"):
    """
    Callback-данные для пагинации списка вакансий.

    Attributes:
        page (int): Номер страницы, на которой находится пользователь.
        page_size (int): Количество вакансий на одной странице.

    Этот callback используется для управления навигацией по списку вакансий
    в inline-кнопках. Значения `page` и `page_size` помогают боту
    определить, какие вакансии показать пользователю.
    """

    page: int
    page_size: int
