from typing import List
from models.base import Base
from models.category import Category
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Vacancy(Base):
    """
    Модель вакансии.

    Таблица `vacancies` хранит информацию о вакансиях, полученных из разных источников,
    включая контактные данные и категорию, к которой относится вакансия.

    Attributes:
        id (int): Уникальный идентификатор вакансии.
        title (str): Заголовок вакансии.
        description (str): Описание вакансии.
        contact_information (str): Контактные данные для связи с отправителем вакансии.
        source (str): Источник вакансии (например, Telegram chat, сайт и т.д.).
        platform_id (str): Идентификатор отправителя вакансии.
        category_id (str): Внешний ключ на категорию вакансии.
        category (Category): Связанная категория вакансии.
        индекс для оптимизации запросов по category_id.
    """

    __tablename__ = "vacancies"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    contact_information: Mapped[str] = mapped_column(String, nullable=False)
    source: Mapped[str] = mapped_column(String, nullable=False)
    platform_id: Mapped[str] = mapped_column(String, nullable=False)

    category_id: Mapped[str] = mapped_column(ForeignKey("categories.id"), index=True)
    category: Mapped["Category"] = relationship(back_populates="vacancies")
    sent_messages: Mapped[List["SentMessage"]] = relationship(
        "SentMessage",
        back_populates="vacancy",
        cascade="all, delete-orphan" # Вот он!
    )