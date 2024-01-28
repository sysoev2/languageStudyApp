from .BaseRepository import BaseRepository
from src.Entity.User import User


class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__()
        self.entity_class = User
