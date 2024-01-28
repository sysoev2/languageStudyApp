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


class CardsGroup(Base):
    __tablename__ = "cards_group"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"))

    # Define the relationship with User
    user = relationship("User")
    cards = relationship("Card", back_populates="card_group")

    def get_active_cards(self) -> list[Card]:
        return [card for card in self.cards if card.next_review_after < datetime.now()]
