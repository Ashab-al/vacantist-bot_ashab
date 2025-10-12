from enum import Enum


class CategorySubscriptionEnum(Enum):
    """
    Перечисление действий пользователя по подписке на категорию.

    Атрибуты:
        SUBSCRIBE (str): Подписка на категорию.
        UNSUBSCRIBE (str): Отписка от категории.
    """

    SUBSCRIBE = "subscribe"
    UNSUBSCRIBE = "unsubscribe"
