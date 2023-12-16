from sqlalchemy import create_engine, Column, Integer, Table, String, Text, TIMESTAMP, ForeignKey, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship
from src.Entity.Base import Base
from .User import User
from .Card import Card


class CardsGroup(Base):
    __tablename__ = 'cards_group'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(String(1023))
    user_id = Column(Integer, ForeignKey('user.id'))

    # Define the relationship with User
    user = relationship("User")
    cards = relationship('Card', secondary=Table(
        "cards_cards_group",
        Base.metadata,
        Column("card_id", ForeignKey("card.id")),
        Column("card_group_id", ForeignKey("cards_group.id")),
    ))
