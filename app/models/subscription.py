from sqlalchemy import (
    String, 
    BigInteger, 
    Integer, 
    Date, 
    Time, 
    ForeignKey, 
    Enum,
    Column,
    Table
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

subscription = Table(
    "subscriptions",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("category_id", ForeignKey("categories.id"), primary_key=True)
)