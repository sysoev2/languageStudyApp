import re

from src.Validator.Base.Validator import Validator


class RegexValidator(Validator):
    def __init__(self, pattern: str, message="Invalid input", *args, **kwargs):
        super().__init__(message, *args, **kwargs)
        self.pattern = pattern
        self.message = message

    def validate(self, value: str):
        return (
            True
            if re.match(self.pattern, value) or not value or not value.strip()
            else self.message
        )
