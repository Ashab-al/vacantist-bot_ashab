from sqlalchemy import String, BigInteger, Integer, Date, Time, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from database import Base
import enum
from models.subscription import subscription

class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)

    vacancies: Mapped[List["Vacancy"]] = relationship(back_populates="category")

    users: Mapped[List["User"]] = relationship("User", secondary=subscription, back_populates="categories")