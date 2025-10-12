from aiogram.filters.callback_data import CallbackData


class OpenVacancyCallback(CallbackData, prefix="open_vacancy"):
    """
    Callback-данные для открытия конкретной вакансии.

    Attributes:
        vacancy_id (int): Уникальный идентификатор вакансии, которую нужно открыть.

    Этот callback используется для inline-кнопок, чтобы бот мог определить,
    какую именно вакансию открыть и показать пользователю подробную информацию.
    """

    vacancy_id: int
