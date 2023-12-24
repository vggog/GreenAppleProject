from sqlalchemy.orm import Session

from src.core.repository import BaseRepository
from src.master.model import RepairOrderModel


class RepairOrderRepository(BaseRepository):
    _model = RepairOrderModel

    def get_repair_order_by_id(
            self,
            order_id: str
    ) -> RepairOrderModel:
        return self.get_object(id=order_id)

    def create_repair_order(self, **kwargs):
        created_object = self._model(**kwargs)

        with Session(self.engine) as session:
            session.add(created_object)
            session.commit()
            session.refresh(created_object)

        return created_object
