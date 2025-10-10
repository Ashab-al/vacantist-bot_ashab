from models.base import Base
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column


class BlackList(Base):
    """
    Модель черного списка.

    Таблица `blacklists` хранит контактную информацию или `platform_id` источника,
    которая была отмечена жалобами.

    Attributes:
        id (int): Уникальный идентификатор записи.
        contact_information (str): Контактные данные (например, Telegram ID или email), 
            которые находятся в черном списке.
        complaint_counter (int): Количество жалоб на данную контактную информацию.
    """

    __tablename__ = "blacklists"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    contact_information: Mapped[str] = mapped_column(
        String, unique=True, nullable=False
    )
    complaint_counter: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
