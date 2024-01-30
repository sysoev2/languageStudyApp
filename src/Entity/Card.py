from typing import TYPE_CHECKING
from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey, REAL
from sqlalchemy.orm import relationship
from src.Entity.Base import Base
from datetime import datetime

if TYPE_CHECKING:
    from src.Entity.CardsGroup import CardsGroup
else:
    CardsGroup = "CardsGroup"


class Card(Base):
    __tablename__ = "card"

    id = Column(Integer, primary_key=True, autoincrement=True)
    front_text = Column(Text, nullable=False)
    back_text = Column(Text, nullable=False)
    next_review_after = Column(
        TIMESTAMP,
        server_default="CURRENT_TIMESTAMP",
        default=lambda: datetime.now(),
        nullable=False,
    )
    last_reviewed_at = Column(TIMESTAMP, default=lambda: datetime.now())
    ease = Column(REAL, default=2.5)
    review_count = Column(Integer, default=0)
    created_by = Column(Integer, ForeignKey("user.id"))
    card_group_id = Column(Integer, ForeignKey("cards_group.id"))

    # Define the relationship with User
    author = relationship("User")
    card_group = relationship("CardsGroup")

    def reviewed(self) -> None:
        self.review_count += 1
        self.next_review_after = datetime.now() + timedelta(days=7)
