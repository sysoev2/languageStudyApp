from datetime import datetime

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    Table,
    String,
    Text,
    TIMESTAMP,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import declarative_base, relationship
from src.Entity.Base import Base
from .User import User
from .Card import Card


class StudyingLog(Base):
    __tablename__ = "studying_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    card_id = Column(Integer, ForeignKey("card.id"))
    created_at = Column(
        TIMESTAMP,
        default=lambda: datetime.now(),
        nullable=False,
    )
    answer = Column(Integer, nullable=False)
    repeat_interval = Column(Integer, nullable=False, default=0)

    card = relationship("Card")
