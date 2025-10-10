from sqlalchemy import ForeignKey, Column, Table
from models.base import Base

subscription = Table(
    "subscriptions",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("category_id", ForeignKey("categories.id"), primary_key=True),
)
"""
Промежуточная таблица для связи многие-ко-многим между пользователями и категориями.

Таблица `subscriptions` хранит подписки пользователей на категории вакансий.

Колонки:
- user_id (FK): ID пользователя.
- category_id (FK): ID категории.
"""
