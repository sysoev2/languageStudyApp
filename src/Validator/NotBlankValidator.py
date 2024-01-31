from src.Validator.Base.Validator import Validator


class NotBlankValidator(Validator):
    def __init__(self, message="This field cannot be blank", *args, **kwargs):
        super().__init__(message, *args, **kwargs)
        self.message = message

    def validate(self, value: str):
        return True if value and value.strip() else self.message
