from dotenv import load_dotenv

from .models import Config
from .db_config import load_db_conf
from .admin_config import load_admin
from .auth_conf import load_auth_conf
from .password_hash import load_password_hash_conf
from .project_setup import load_project_set_up


def load_config() -> Config:
    load_dotenv()
    return Config(
        db=load_db_conf(),
        admin=load_admin(),
        auth=load_auth_conf(),
        password_hash=load_password_hash_conf(),
        project_setup=load_project_set_up(),
    )
