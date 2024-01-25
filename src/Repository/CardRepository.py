from datetime import datetime

from .BaseRepository import BaseRepository
from src.Entity.Card import Card
from src.Entity.CardsGroup import CardsGroup
from sqlalchemy import and_


class CardRepository(BaseRepository):
    MAX_CARDS_PER_GAME = 20

    def __init__(self):
        super().__init__()
        self.entity_class = Card

    def get_cards_to_study_by_group_name(self, group_id: int) -> list[Card]:
        return (
            self._session.query(self.entity_class)
            .where(
                and_(
                    Card.card_group_id == group_id,
                    Card.next_review_after < datetime.now(),
                )
            )
            .all()
        )
