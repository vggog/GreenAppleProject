from dataclasses import dataclass


@dataclass
class PasswordDataType:
    hash: str
    salt: str
