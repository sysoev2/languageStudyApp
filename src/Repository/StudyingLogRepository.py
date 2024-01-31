from typing import Any, Sequence

from .BaseRepository import BaseRepository
from src.Entity.StudyingLog import StudyingLog
from sqlalchemy.sql import func
from sqlalchemy import select, Row
from src.Entity.CardsGroup import CardsGroup
from src.Entity.Card import Card


class StudyingLogRepository(BaseRepository[StudyingLog]):
    def __init__(self):
        super().__init__()
        self.entity_class = StudyingLog

    def get_log_group_by_day(
        self, user_id: int
    ) -> Sequence[Row[tuple[Any, ...] | Any]]:
        return self._session.execute(
            select(
                func.date(StudyingLog.created_at),
                CardsGroup.name,
                CardsGroup.id,
                func.count(StudyingLog.id),
            )
            .join(StudyingLog.card)
            .join(Card.card_group)
            .filter(StudyingLog.card.has(created_by=user_id))
            .group_by(func.date(StudyingLog.created_at))
            .order_by(func.date(StudyingLog.created_at).desc())
        ).all()

    def get_logs_by_card_group_id_and_date(
        self,
        card_group_id: int,
        date: str,
    ):
        return (
            self._get_query_builder()
            .join(StudyingLog.card)
            .join(Card.card_group)
            .filter(
                StudyingLog.card.has(card_group_id=card_group_id),
                func.date(StudyingLog.created_at) == date,
            )
            .order_by(StudyingLog.created_at.desc())
            .all()
        )
