from sqlalchemy import String, BigInteger, Integer, Date, Time, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
import enum


class BlackList(Base):
    __tablename__ = 'blacklists'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    contact_information: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    complaint_counter: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

