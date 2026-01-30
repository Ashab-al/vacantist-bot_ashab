from typing import List

from models.base import Base
from models.user import User
from models.vacancy import Vacancy
from sqlalchemy import Integer, String, BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class SentMessage(Base):
    __tablename__ = "sent_messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Внешние ключи обязательны для работы relationship
    vacancy_id: Mapped[int] = mapped_column(ForeignKey("vacancies.id", ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    # Telegram ID сообщений могут быть большими, BigInteger надежнее
    message_id: Mapped[int] = mapped_column(BigInteger, nullable=False)

    # Сами связи
    vacancy: Mapped["Vacancy"] = relationship("Vacancy", back_populates="sent_messages")
    user: Mapped["User"] = relationship("User", back_populates="sent_messages")