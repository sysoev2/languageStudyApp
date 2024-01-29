from .BaseRepository import BaseRepository
from src.Entity.StudyingLog import StudyingLog


class StudyingLogRepository(BaseRepository[StudyingLog]):
    def __init__(self):
        super().__init__()
        self.entity_class = StudyingLog
