from sqlalchemy.orm import Session

from src.core.repository import BaseRepository
from src.master.model import RepairOrderModel


class RepairOrderRepository(BaseRepository):
    _model = RepairOrderModel

    def get_repair_order_by_id(
            self,
            order_id: int
    ) -> RepairOrderModel:
        return self.get_object(id=order_id)

    def create_repair_order(self, **kwargs):
        created_object = self._model(**kwargs)

        with Session(self.engine) as session:
            session.add(created_object)
            session.commit()
            session.refresh(created_object)

        return created_object

    def update_status_of_repair_order(
            self,
            repair_order_id: int,
            status: str
    ) -> RepairOrderModel:
        self.update_object(object_id=repair_order_id, status=status)

        return self.get_repair_order_by_id(repair_order_id)
