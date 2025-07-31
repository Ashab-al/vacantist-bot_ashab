from __future__ import annotations
import datetime
from sqlalchemy import (
    TIMESTAMP,
    Index,
    String,
    ForeignKey,
    UniqueConstraint,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
