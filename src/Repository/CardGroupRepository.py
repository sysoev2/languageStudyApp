from .BaseRepository import BaseRepository
from src.Entity.CardsGroup import CardsGroup


class CardGroupRepository(BaseRepository[CardsGroup]):
    def __init__(self):
        super().__init__()
        self.entity_class = CardsGroup
