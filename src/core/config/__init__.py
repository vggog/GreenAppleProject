from dotenv import load_dotenv

from .models import Config
from .db_config import load_db_conf


def load_config() -> Config:
    load_dotenv()
    return Config(
        db=load_db_conf(),
    )
