from dataclasses import dataclass


@dataclass
class UserDTO:
    username: str
    password: str
    password_repeat: str
