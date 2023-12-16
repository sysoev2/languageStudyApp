from abc import ABC, abstractmethod
from sqlalchemy.orm import Session


class BaseRepository(ABC):
    def __init__(self, session: Session, entity_class):
        self.session = session
        self.entity_class = entity_class

    @abstractmethod
    def create(self, **kwargs):
        entity = self.entity_class(**kwargs)
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity

    @abstractmethod
    def get_all(self):
        return self.session.query(self.entity_class).all()

    @abstractmethod
    def get_by_id(self, entity_id):
        return self.session.query(self.entity_class).filter(self.entity_class.id == entity_id).first()
