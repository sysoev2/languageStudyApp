from abc import ABC


class Validator(ABC):
    def __init__(self, message: str, *args, **kwargs):
        self.message = message

    def validate(self, value) -> str | bool:
        pass
