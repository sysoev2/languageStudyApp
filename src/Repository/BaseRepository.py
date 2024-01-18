from abc import ABC
from sqlalchemy.orm import Session
from index.database import Database
from src.Entity.Base import Base


class BaseRepository(ABC):
    __session: Session
    entity_class = None

    def __init__(self):
        self.__session = Database().get_session()

    def create(self, **kwargs) -> None:
        entity = self.entity_class(**kwargs)
        self.__session.add(entity)
        self.__session.commit()
        self.__session.refresh(entity)
        return entity

    def save(self) -> None:
        self.__session.commit()

    def delete(self, entity: Base) -> None:
        self.__session.delete(entity)
        self.__session.commit()

    def get_all(self) -> list[Base]:
        return self.__session.query(self.entity_class).all()

    def get_by_id(self, entity_id) -> Base | None:
        return (
            self.__session.query(self.entity_class)
            .filter(self.entity_class.id == entity_id)
            .one_or_none()
        )

    def get_all_by(self, **kwargs) -> list[Base]:
        query = self.__session.query(self.entity_class)
        for attr, value in kwargs.items():
            query = query.filter(getattr(self.entity_class, attr) == value)
        return query.all()

    def get_one_by(self, **kwargs) -> Base | None:
        query = self.__session.query(self.entity_class)
        for attr, value in kwargs.items():
            query = query.filter(getattr(self.entity_class, attr) == value)
        return query.one_or_none()
