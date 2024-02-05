import re

from sqlalchemy.orm import Session

from index.database import Database
from src.Entity.Base import Base
from src.Validator.Base.Validator import Validator
from sqlalchemy import func


class UniqueEntityValidator(Validator):
    _session: Session
    fields: list
    entity_type = None

    def __init__(
        self,
        fields: list,
        entity_type=None,
        message="Entity should be unique",
        *args,
        **kwargs
    ):
        super().__init__(message, *args, **kwargs)
        self.entity_type = entity_type
        self.fields = fields
        self._session = Database().get_session()
        self.message = message

    def validate(self, model: Base):
        entity_type = self.entity_type if self.entity_type else model.__class__
        query = self._session.query(entity_type)
        for field in self.fields:
            value = getattr(model, field)
            if isinstance(value, str):
                query = query.filter(
                    func.lower(getattr(entity_type, field)) == func.lower(value)
                )
            else:
                query = query.filter(getattr(entity_type, field) == value)
        if hasattr(model, "id"):
            query = query.filter(entity_type.id != model.id)
        return True if not query.first() else self.message
