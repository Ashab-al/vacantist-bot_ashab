from sqlalchemy import (
    String, 
    BigInteger, 
    Integer, 
    Date, 
    Time, 
    ForeignKey, 
    Enum,
    Column
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
from enums.bot_status_enum import BotStatusEnum
from models.subscription import subscription
from typing import List

class User(Base):
    __tablename__ = 'users'

    DEFAULT_POINT=0
    DEFAULT_BONUS=5
    COUNT_FOR_FULL_BATTERY = 5
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    platform_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    username: Mapped[str] = mapped_column(String(100), nullable=True, unique=True)
    email: Mapped[str] = mapped_column(String(100), nullable=True, unique=True)
    phone: Mapped[str] = mapped_column(String(100), nullable=True, unique=True)
    point: Mapped[int] = mapped_column(Integer, default=DEFAULT_POINT, nullable=False)
    bonus: Mapped[int] = mapped_column(Integer, default=DEFAULT_BONUS, nullable=False)
    bot_status: Mapped[BotStatusEnum] = mapped_column(Enum(BotStatusEnum, name='bot_status'), nullable=False)

    categories: Mapped[List["Category"]] = relationship("Category", secondary=subscription, back_populates="users")
