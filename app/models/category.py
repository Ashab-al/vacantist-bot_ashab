from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from models.base import Base
from models.subscription import subscription
from models.user import User
from typing import List


class Category(Base):
    """
    Модель категории вакансий.

    Таблица `categories` хранит категории вакансий и связи с пользователями.

    Attributes:
        id (int): Уникальный идентификатор категории.
        name (str): Название категории (уникальное, обязательно к заполнению).
        vacancies (List[Vacancy]): Список вакансий, относящихся к этой категории.
        users (List[User]): Список пользователей, подписанных на эту категорию.
    """

    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)

    vacancies: Mapped[List["Vacancy"]] = relationship(back_populates="category")

    users: Mapped[List["User"]] = relationship(
        "User", secondary=subscription, back_populates="categories"
    )
