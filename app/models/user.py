from typing import List

from enums.bot_status_enum import BotStatusEnum
from models.base import Base
from models.subscription import subscription
from sqlalchemy import BigInteger, Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base):
    """
    Модель пользователя.

    Таблица `users` хранит информацию о пользователях Telegram и их активности
    в системе, включая количество поинтов, бонусов, статус и подписки на категории.

    Константы:
        DEFAULT_POINT (int): Начальное количество поинтов пользователя.
        DEFAULT_BONUS (int): Начальное количество бонусов пользователя.
        COUNT_FOR_FULL_BATTERY (int): Количество поинтов для полной «зарядки» поинтов
            (учитывается при выборе смайлика).

    Attributes:
        id (int): Уникальный идентификатор пользователя.
        platform_id (int): ID пользователя в Telegram (уникальный).
        first_name (str): Имя пользователя.
        username (str | None): Username пользователя в Telegram.
        email (str | None): Почта пользователя.
        phone (str | None): Телефон пользователя.
        point (int): Количество поинтов у пользователя.
        bonus (int): Количество бонусных поинтов у пользователя.
        bot_status (BotStatusEnum): Статус пользователя в системе.
        categories (List[Category]): Список категорий, на которые подписан пользователь.
    """

    __tablename__ = "users"

    DEFAULT_POINT = 0
    DEFAULT_BONUS = 5
    COUNT_FOR_FULL_BATTERY = 5

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    platform_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    username: Mapped[str] = mapped_column(String(100), nullable=True, unique=True)
    email: Mapped[str] = mapped_column(String(100), nullable=True, unique=True)
    phone: Mapped[str] = mapped_column(String(100), nullable=True, unique=True)
    point: Mapped[int] = mapped_column(Integer, default=DEFAULT_POINT, nullable=False)
    bonus: Mapped[int] = mapped_column(Integer, default=DEFAULT_BONUS, nullable=False)
    bot_status: Mapped[BotStatusEnum] = mapped_column(
        Enum(BotStatusEnum, name="bot_status"), nullable=False, index=True
    )

    categories: Mapped[List["Category"]] = relationship(  # noqa: F821 # pyright: ignore[reportUndefinedVariable]
        "Category", secondary=subscription, back_populates="users"
    )
