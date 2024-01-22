from .BaseRepository import BaseRepository
from src.Entity.Card import Card


class CardRepository(BaseRepository):
    def __init__(self):
        super().__init__()
        self.entity_class = Card
