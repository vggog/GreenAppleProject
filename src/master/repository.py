from src.core.repository import BaseRepository
from src.master.model import MasterModel


class Repository(BaseRepository):
    _model = MasterModel
