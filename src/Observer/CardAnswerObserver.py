from src.Observer.AbstractObserver import AbstractObserver
from src.Repository.StudyingLogRepository import StudyingLogRepository
from src.Entity.StudyingLog import StudyingLog


class CardAnswerObserver(AbstractObserver):
    EVENT_NAME = "card_answer"

    def update(self, observable, *args, **kwargs):
        repository = StudyingLogRepository()
        repository.persist(
            StudyingLog(
                card=kwargs["card"],
                answer=kwargs["answer"],
                repeat_interval=kwargs["repeat_interval"],
            )
        )
        repository.save()
