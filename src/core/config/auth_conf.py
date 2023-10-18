import os
from .models import Auth


def load_auth_conf() -> Auth:
    return Auth(
        secret_key=os.getenv("SECRET_KEY"),
        algorithm=os.getenv("ALGORITHM"),
        access_token_operating_time=int(
            os.getenv("ACCESS_TOKEN_OPERATING_TIME")
        ),
        refresh_token_operating_time=int(
            os.getenv("REFRESH_TOKEN_OPERATING_TIME")
        ),
    )
