from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from src.core.config import load_config


class Authorization:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    auth_conf = load_config().auth

    def verify_password(self, password, hashed_password):
        return self.pwd_context.verify(password, hashed_password)

    def create_jwt_token(self, data):
        """
        Creating jwt token with specific data.
        """
        return jwt.encode(
            data,
            self.auth_conf.secret_key,
            algorithm=self.auth_conf.algorithm
        )

    def create_access_token(
            self,
            data: dict,
    ):
        """
        Creating an access token with specific data and operating time.
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(
            seconds=self.auth_conf.access_token_operating_time
        )

        to_encode["exp"] = expire
        return self.create_jwt_token(to_encode)

    def create_refresh_token(
            self,
            data: dict,
    ):
        """
        Creating a refresh token with specific data and operating time.
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(
            seconds=self.auth_conf.refresh_token_operating_time
        )

        to_encode["exp"] = expire
        return jwt.encode(
            to_encode,
            self.auth_conf.secret_key,
            algorithm=self.auth_conf.algorithm
        )
