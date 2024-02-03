from abc import ABC
from typing import Any

from src.Entity.Card import Card
from src.Validator.Base.Validator import Validator


class ComplexValidator(ABC):
    _FIELD_NAME_MAP: dict[str, str]
    validators: dict[str, list[Validator] | Validator]

    def validate(self, value: object) -> dict[str, str] | bool:
        errors = {}
        for key, validators in self.validators.items():
            error_field = (
                self._FIELD_NAME_MAP.get(key) if self._FIELD_NAME_MAP.get(key) else key
            )
            if isinstance(validators, list):
                for validator in validators:
                    error = validator.validate(self.get_attribute(value, key))
                    if error is not True:
                        errors[error_field] = error
                        break
            else:
                error = validators.validate(self.get_attribute(value, key))
                if error is not True:
                    errors[error_field] = error
        return errors if errors else True

    def get_attribute(self, value: object, attribute: str) -> Any:
        return (
            getattr(value, attribute)
            if value.__class__.__name__ != attribute
            else value
        )
