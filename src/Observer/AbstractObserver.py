from abc import ABC, abstractmethod


class AbstractObserver(ABC):
    EVENT_NAME: str

    @abstractmethod
    def update(self, observable, *args, **kwargs):
        pass
