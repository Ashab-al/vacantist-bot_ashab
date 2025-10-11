from enum import Enum


class CheckVacancyEnum(Enum):
    """
    Перечисление статусов проверки вакансии.

    Атрибуты:
        WARNING (str): Вакансия содержит предупреждения.
        OPEN_VACANCY (str): Вакансия открыта и готова к публикации.
    """

    WARNING = "warning"
    OPEN_VACANCY = "open_vacancy"
