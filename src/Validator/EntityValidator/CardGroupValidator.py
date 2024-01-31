from src.DTO.UserDTO import UserDTO
from src.Validator.Base.ComplexValidator import ComplexValidator
from src.Validator.Base.Validator import Validator
from src.Validator.NotBlankValidator import NotBlankValidator
from src.Validator.RegexValidator import RegexValidator


class CardGroupValidator(ComplexValidator):
    _FIELD_NAME_MAP = {"name": "Title"}

    def __init__(self):
        super().__init__()
        self.validators = {
            "name": NotBlankValidator(),
        }
