from abc import ABC
from multipledispatch import dispatch
from sqlalchemy.orm import Session, Query
from index.database import Database
from src.Entity.Base import Base
from typing import Any, TypeVar, Generic, List

T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    _session: Session
    entity_class: T

    def __init__(self):
        self._session = Database().get_session()

    def create(self, **kwargs) -> T:
        entity = self.entity_class(**kwargs)
        self._session.add(entity)
        self._session.commit()
        self._session.refresh(entity)
        return entity

    def save(self) -> None:
        self._session.commit()

    @dispatch(Base)
    def delete(self, entity: T) -> None:
        self._session.delete(entity)
        self._session.commit()

    @dispatch(int)
    def delete(self, entity_id: int) -> None:
        self._get_query_builder().filter_by(id=entity_id).delete()
        self._session.commit()

    def get_all(self) -> List[T]:
        return self._get_query_builder().all()

    def get_by_id(self, entity_id: int) -> T | None:
        return (
            self._get_query_builder()
            .filter(self.entity_class.id == entity_id)
            .one_or_none()
        )

    def get_all_by(self, **kwargs: dict[str, Any]) -> List[T]:
        query = self._get_query_builder()
        for attr, value in kwargs.items():
            query = query.filter(getattr(self.entity_class, attr) == value)
        return query.all()

    def get_one_by(self, **kwargs: dict[str, Any]) -> T | None:
        query = self._get_query_builder()
        for attr, value in kwargs.items():
            query = query.filter(getattr(self.entity_class, attr) == value)
        return query.one_or_none()

    def _get_query_builder(self) -> Query:
        return self._session.query(self.entity_class)
