from abc import ABC
from src.Observer.AbstractObserver import AbstractObserver


class AbstractObservable(ABC):
    __observers: list[AbstractObserver]

    def __init__(self):
        self.__observers = []

    def add_observer(self, observer: AbstractObserver) -> None:
        self.__observers.append(observer)

    def remove_observer(self, observer: AbstractObserver) -> None:
        self.__observers.remove(observer)

    def notify_observers(self, event: str, *args, **kwargs) -> None:
        for observer in self.__observers:
            if observer.EVENT_NAME == event:
                observer.update(self, *args, **kwargs)
