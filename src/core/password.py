import os
import hashlib

from src.core.datatype_models import PasswordDataType
from src.core.config import load_config


class Password:
    hash_conf = load_config().password_hash

    def generate_password_hash(self, password: str) -> PasswordDataType:
        salt = os.urandom(self.hash_conf.salt_length)

        password_hash = hashlib.pbkdf2_hmac(
            self.hash_conf.algorithm,
            password.encode(),
            salt,
            self.hash_conf.iterations
        )

        return PasswordDataType(
            hash=password_hash.hex(),
            salt=salt.hex(),
        )
