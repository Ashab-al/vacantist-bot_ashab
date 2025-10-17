from models.base import Base
from sqlalchemy import Column, ForeignKey, Index, Table

subscription = Table(
    "subscriptions",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("category_id", ForeignKey("categories.id"), primary_key=True),
    Index("idx_subscriptions_category_id", "category_id"),
    Index("idx_subscriptions_user_id", "user_id")

)
"""
Промежуточная таблица для связи многие-ко-многим между пользователями и категориями.

Таблица `subscriptions` хранит подписки пользователей на категории вакансий.

Колонки:
- user_id (FK): ID пользователя.
- category_id (FK): ID категории.
- Индексы для оптимизации запросов по user_id и category_id.
"""
