import enum


class BotStatusEnum(enum.Enum):
    """
    Перечисление статусов пользователя в боте.

    Атрибуты:
        WORKS (str): Пользователь активен и взаимодействует с ботом.
        BOT_BLOCKED (str): Пользователь заблокировал бота или недоступен для взаимодействия.
    """

    WORKS = "WORKS"
    BOT_BLOCKED = "BOT_BLOCKED"
