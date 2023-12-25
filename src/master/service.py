from src.core.service import BaseService
from src.master.repository import Repository
from src.master.repair_order_repository import RepairOrderRepository
from starlette import status
from src.core.authorization import Authorization
from src.core.password import Password
from src.master.model import MasterModel, RepairOrderModel
from src.master.schemas import CreateRepairOrderSchema


class Servise(BaseService):
    repository = Repository()
    repair_order_repository = RepairOrderRepository()
    auth = Authorization()
    password = Password()

    def get_master_by_phone(self, phone: str) -> MasterModel | None:
        """
        Получить модель мастера по номеру телефона.
        :param phone: номер телефона мастера
        :return: мастер(MasterModel)
        """
        return self.repository.get_object(phone=phone)

    def get_master(self, phone: str, password: str) -> tuple[status, str | MasterModel]:
        master: MasterModel = self.repository.get_object(phone=phone)
        if not master:
            return status.HTTP_404_NOT_FOUND, 'master not found'

        if not self.password.check_password(password, master.salt, master.password):
            return status.HTTP_403_FORBIDDEN, 'password is not a correct!'
        return status.HTTP_200_OK, master

    def create_repair_order(
            self,
            repair_order: CreateRepairOrderSchema,
            phone_number: str
    ) -> RepairOrderModel:
        master = self.get_master_by_phone(phone_number)

        if not master:
            ...

        return self.repair_order_repository.create_repair_order(
            **repair_order.model_dump(),
            master_id=master.id,
        )

    def get_all_repair_orders(self) -> list[RepairOrderModel]:
        return self.repair_order_repository.get_all_datas_from_table()

    def get_repair_order(
            self,
            repair_order_id: int
    ) -> RepairOrderModel | None:
        repair_order = self.repair_order_repository.get_repair_order_by_id(
            repair_order_id
        )

        if repair_order is None:
            return None

        master = self.repository.get_master_by_id(repair_order.master_id)
        repair_order.master = master

        return repair_order
