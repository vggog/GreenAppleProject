from src.core.service import BaseService
from src.master.repository import Repository
from src.master.repair_order_repository import RepairOrderRepository
from starlette import status
from src.core.authorization import Authorization
from src.core.password import Password
from src.master.model import MasterModel, RepairOrderModel
from src.master.schemas import (
    CreateRepairOrderSchema, UpdatedRepairOrderSchema
)
from src.core.config import load_config
from src.master.receipt_generator import ReceiptGenerator
from src.master.status_changed_repository import StatusChangedRepository


class Servise(BaseService):
    repository = Repository()
    repair_order_repository = RepairOrderRepository()
    status_changed_repository = StatusChangedRepository()
    auth = Authorization()
    password = Password()
    project_set_up = load_config().project_setup
    receipt_generator = ReceiptGenerator()

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
            master: MasterModel,
    ) -> RepairOrderModel:
        created_repair_order = self.repair_order_repository.create_repair_order(
            **repair_order.model_dump(),
        )

        self.status_changed_repository.add_status_change_row(
            status=created_repair_order.status,
            repair_order_id=created_repair_order.id,
            master_id=master.id
        )

        return created_repair_order

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

        return repair_order

    def update_repair_order_info(
            self,
            repair_order_id: int,
            updated_repair_order: UpdatedRepairOrderSchema,
            master: MasterModel,
    ) -> tuple[status, RepairOrderModel | str]:
        statuses = self.project_set_up.order_statuses

        if updated_repair_order.status not in statuses:
            statuses_string = ", ".join(statuses)
            return (
                status.HTTP_400_BAD_REQUEST,
                "Статус заказа должен быть: " + statuses_string
            )

        repair_order = self.get_repair_order(
            repair_order_id
        )

        if repair_order is None:
            return (
                status.HTTP_404_NOT_FOUND,
                "Repair order not found"
            )

        self.repair_order_repository.update_status_of_repair_order(
            repair_order_id,
            updated_repair_order.status,
        )

        self.status_changed_repository.add_status_change_row(
            status=updated_repair_order.status,
            repair_order_id=repair_order_id,
            master_id=master.id
        )

        return (
            status.HTTP_200_OK,
            self.get_repair_order(repair_order_id)
        )

    def generate_receipt(self, repair_order_id):
        """
        :param repair_order_id:
        :return:
        """
        repair_order = self.get_repair_order(repair_order_id)

        if repair_order is None:
            return (
                status.HTTP_404_NOT_FOUND,
                "Repair order not found"
            )

        return (
            status.HTTP_200_OK,
            self.receipt_generator.get_receipt(repair_order)
        )
