from datetime import datetime

from .BaseRepository import BaseRepository
from src.Entity.Card import Card
from src.Entity.CardsGroup import CardsGroup
from sqlalchemy.orm.query import Query
from sqlalchemy import and_


class CardRepository(BaseRepository[Card]):
    def __init__(self):
        super().__init__()
        self.entity_class = Card

    def get_cards_to_study_by_group_name_qb(self, group_id: int) -> Query:
        return self._session.query(self.entity_class).where(
            and_(
                Card.card_group_id == group_id,
                Card.next_review_after < datetime.now(),
            )
        )

    def get_cards_to_study_by_group_name(self, group_id: int) -> list[Card]:
        return self.get_cards_to_study_by_group_name_qb(group_id).all()

    def get_cards_to_study_by_group_name_count(self, group_id: int) -> int:
        return self.get_cards_to_study_by_group_name_qb(group_id).count()
