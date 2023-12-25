from src.core.repository import BaseRepository
from src.master.model import MasterModel


class Repository(BaseRepository):
    _model = MasterModel

    def get_master_by_id(self, master_id: int) -> MasterModel:
        return self.get_object(id=master_id)
