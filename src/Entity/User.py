from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.Entity.Base import Base
from .Card import Card
from sqlalchemy.ext.hybrid import hybrid_property
import bcrypt

from ..DTO.UserDTO import UserDTO


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True)
    _password = Column(String, name="password")

    # Define the relationship with Post
    cards = relationship("Card", back_populates="author")

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(12))

    @staticmethod
    def create_from_dto(dto: UserDTO) -> "User":
        return User(username=dto.username, password=dto.password)
