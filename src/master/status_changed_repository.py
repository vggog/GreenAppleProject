from src.core.repository import BaseRepository
from src.master.model import StatusChangedModel


class StatusChangedRepository(BaseRepository):
    _model = StatusChangedModel

    def add_status_change_row(
            self, status: str, repair_order_id: int, master_id: int
    ):
        self.create(
            status=status,
            master_id=master_id,
            repair_order_id=repair_order_id,
        )
