from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from src.Entity.Base import Base


class Card(Base):
    __tablename__ = "card"

    id = Column(Integer, primary_key=True, autoincrement=True)
    front_text = Column(Text, nullable=False)
    back_text = Column(Text, nullable=False)
    deck_name = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP", nullable=False)
    last_reviewed_at = Column(TIMESTAMP)
    ease = Column(Integer, default=2)
    review_count = Column(Integer, default=0)
    created_by = Column(Integer, ForeignKey("user.id"))

    # Define the relationship with User
    author = relationship("User")
