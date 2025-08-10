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
from app.database import Base


class Vacancy(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(String, nullable=False)
    contact_information: Mapped[str] = mapped_column(String, nullable=False)
    source: Mapped[str] = mapped_column(String, nullable=False)
    platform_id: Mapped[str] = mapped_column(String, nullable=False)
    
    category_id: Mapped[str] = mapped_column(ForeignKey("categories.id", nullable=False))
    category: Mapped["Category"] = relationship(back_populates="vacancies")