from dotenv import load_dotenv

from .models import Config
from .db_config import load_db_conf
from .admin_config import load_admin
from .auth_conf import load_auth_conf


def load_config() -> Config:
    load_dotenv()
    return Config(
        db=load_db_conf(),
        admin=load_admin(),
        auth=load_auth_conf(),
    )
