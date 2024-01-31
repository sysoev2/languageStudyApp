from datetime import datetime, timedelta

from .BaseRepository import BaseRepository
from src.Entity.Card import Card
from src.Entity.StudyingLog import StudyingLog
from sqlalchemy.orm.query import Query
from sqlalchemy import and_, between


class CardRepository(BaseRepository[Card]):
    __CARDS_TO_STUDY_PER_DAY_LIMIT = 20
    entity_class = Card

    def _get_cards_to_study_by_group_id_qb(self, group_id: int) -> Query:
        today = datetime.now().date()
        tomorrow = today + timedelta(days=1)
        limit = (
            self._get_query_builder()
            .join(StudyingLog)
            .where(
                and_(
                    Card.card_group_id == group_id,
                    between(StudyingLog.created_at, today, tomorrow),
                    StudyingLog.repeat_interval > 0,
                )
            )
            .count()
        )
        limit = self.__CARDS_TO_STUDY_PER_DAY_LIMIT - limit
        limit = limit if limit > 0 else 0
        return (
            self._get_query_builder()
            .where(
                and_(
                    Card.card_group_id == group_id,
                    Card.next_review_after < datetime.now(),
                )
            )
            .limit(limit)
        )

    def get_cards_to_study_by_group_id(self, group_id: int) -> list[Card]:
        return self._get_cards_to_study_by_group_id_qb(group_id).all()

    def get_cards_to_study_by_group_id_count(self, group_id: int) -> int:
        return self._get_cards_to_study_by_group_id_qb(group_id).count()

    def get_cards_by_group_id(self, group_id: int) -> list[Card]:
        return self._get_query_builder().where(Card.card_group_id == group_id).all()
