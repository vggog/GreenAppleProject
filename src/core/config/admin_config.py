import os
from src.core.config.models import Admin


def load_admin() -> Admin:
    return Admin(
        username=os.getenv("ADMIN_USERNAME"),
        password=os.getenv("ADMIN_PASSWORD")
    )
