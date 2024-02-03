from src.DTO.UserDTO import UserDTO
from src.Entity.User import User
from src.Validator.Base.ComplexValidator import ComplexValidator
from src.Validator.NotBlankValidator import NotBlankValidator
from src.Validator.RegexValidator import RegexValidator
from src.Validator.UniqueEntityValidator import UniqueEntityValidator


class UserDTOValidator(ComplexValidator):
    _FIELD_NAME_MAP = {
        "username": "Username",
        "password": "Password",
        "password_repeat": "Repeat Password",
        UserDTO.__name__: "Username",
    }

    def __init__(self, message="This field cannot be blank", *args, **kwargs):
        super().__init__()
        self.message = message
        password_validators = [
            NotBlankValidator(),
            RegexValidator(
                r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$",
                "Password must contain at least 8 characters, one uppercase letter and one number",
            ),
        ]
        self.validators = {
            UserDTO.__name__: UniqueEntityValidator(
                ["username"], User, "Username already exists"
            ),
            "username": NotBlankValidator(),
            "password": password_validators,
            "password_repeat": password_validators,
        }
