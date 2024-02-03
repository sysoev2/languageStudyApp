from src.DTO.UserDTO import UserDTO
from src.Entity.Card import Card
from src.Repository.CardRepository import CardRepository
from src.Validator.Base.ComplexValidator import ComplexValidator
from src.Validator.Base.Validator import Validator
from src.Validator.NotBlankValidator import NotBlankValidator
from src.Validator.RegexValidator import RegexValidator
from src.Validator.UniqueEntityValidator import UniqueEntityValidator


class CardValidator(ComplexValidator):
    _FIELD_NAME_MAP = {
        "front_text": "Front text",
        "back_text": "Back text",
    }

    def __init__(self):
        super().__init__()
        self.validators = {
            Card.__name__: UniqueEntityValidator(
                ["front_text", "back_text", "card_group"]
            ),
            "front_text": NotBlankValidator(),
            "back_text": NotBlankValidator(),
        }
