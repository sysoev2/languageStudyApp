from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from index.database import Database


class BaseRepository(ABC):
    session: Session
    entity_class = None

    def __init__(self):
        self.session = Database().get_session()

    def create(self, **kwargs):
        entity = self.entity_class(**kwargs)
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity

    def get_all(self):
        return self.session.query(self.entity_class).all()

    def get_by_id(self, entity_id):
        return self.session.query(self.entity_class).filter(self.entity_class.id == entity_id).first()

    def get_all_by(self, **kwargs):
        query = self.session.query(self.entity_class)
        for attr, value in kwargs.items():
            query = query.filter(getattr(self.entity_class, attr) == value)
        return query.all()

    def get_one_by(self, **kwargs):
        query = self.session.query(self.entity_class)
        for attr, value in kwargs.items():
            query = query.filter(getattr(self.entity_class, attr) == value)
        return query.one_or_none()

