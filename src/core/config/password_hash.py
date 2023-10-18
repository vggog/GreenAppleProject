import os

from src.core.config.models import PasswordHashConfig


def load_password_hash_conf() -> PasswordHashConfig:
    return PasswordHashConfig(
        algorithm=os.getenv("HASH_ALGORITHM"),
        salt_length=int(os.getenv("SALT_LENGTH")),
        iterations=int(os.getenv("ITERATIONS")),
    )
