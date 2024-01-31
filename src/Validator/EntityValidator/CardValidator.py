from src.DTO.UserDTO import UserDTO
from src.Validator.Base.ComplexValidator import ComplexValidator
from src.Validator.Base.Validator import Validator
from src.Validator.NotBlankValidator import NotBlankValidator
from src.Validator.RegexValidator import RegexValidator


class CardValidator(ComplexValidator):
    _FIELD_NAME_MAP = {"front_text": "Front text", "back_text": "Back text"}

    def __init__(self):
        super().__init__()
        self.validators = {
            "front_text": NotBlankValidator(),
            "back_text": NotBlankValidator(),
        }
