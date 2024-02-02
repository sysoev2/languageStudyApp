from typing import TYPE_CHECKING

from src.DTO.UserDTO import UserDTO
from src.Validator.Base.ComplexValidator import ComplexValidator
from src.Validator.Base.Validator import Validator
from src.Validator.NotBlankValidator import NotBlankValidator
from src.Validator.RegexValidator import RegexValidator
from src.Validator.UniqueEntityValidator import UniqueEntityValidator
from src.Entity.CardsGroup import CardsGroup


class CardGroupValidator(ComplexValidator):
    _FIELD_NAME_MAP = {"name": "Title", CardsGroup.__name__: "Card Group"}

    def __init__(self):
        super().__init__()
        self.validators = {
            CardsGroup.__name__: UniqueEntityValidator(["name", "user"]),
            "name": NotBlankValidator(),
        }
