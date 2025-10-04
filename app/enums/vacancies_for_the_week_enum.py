from enum import Enum


class VacanciesForTheWeekStatusEnum(Enum):
    """
    Статусы формирования списка вакансий за неделю.

    Атрибуты:
        SUBSCRIBED_CATEGORIES_EMPTY (str): У пользователя нет подписок на категории.
        VACANCY_LIST_EMPTY (str): Нет доступных вакансий за выбранный период.
        OK (str): Вакансии успешно найдены и готовы к отображению.
    """
    SUBSCRIBED_CATEGORIES_EMPTY = 'subscribed_categories_empty'
    VACANCY_LIST_EMPTY = 'vacancy_list_empty'
    OK = 'ok'