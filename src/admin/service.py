import re

from starlette import status

from src.core.config import load_config
from src.admin.repository import Repository
from src.core.service import BaseService
from src.admin.schemas import (
    MasterInfoWithPassword, MasterInfoSchema, MasterInfoWithIdSchema,
    MasterUpdateSchema
)
from src.core.password import Password
from src.core.utils import delete_none_value_from_dict


class Service(BaseService):
    repository = Repository()
    hash_password = Password()
    admin_conf = load_config().admin
    project_setup = load_config().project_setup

    def is_valid_admin_conf(self, username: str, password: str) -> bool:
        """
        Checking username and password with admin configurations.
        :param username:
        :param password:
        :return:
        """
        return (
            (username == self.admin_conf.username)
            and
            (password == self.admin_conf.password)
        )

    def is_admin(self, username: str) -> bool:
        """

        :param username:
        :return:
        """
        return username == self.admin_conf.username

    @staticmethod
    def validate_phone(phone: str) -> bool:
        return bool(
            re.match(
                r"^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$",
                phone
            )
        )

    def validate_password(self, password: str) -> bool:
        return len(password) > self.project_setup.password_length

    def add_master(self, master: MasterInfoWithPassword) -> tuple[bool, str]:
        if not Service.validate_phone(master.phone):
            return False, "The entered phone number is incorrect."

        if not self.validate_password(master.password):
            return False, "Small password length."

        pass_hash = self.hash_password.generate_password_hash(
            password=master.password
            )

        self.repository.create(
            name=master.name,
            surname=master.surname,
            phone=master.phone,
            password=pass_hash.hash,
            salt=pass_hash.salt
        )

        return True, ""

    def get_all_masters(self) -> list[MasterInfoWithIdSchema]:
        """
        Return all masters in the database.
        :return:
        """
        master_objects = self.repository.get_all_datas_from_table()
        masters = []
        for master in master_objects:
            masters.append(
                MasterInfoWithIdSchema(
                    id=master.id,
                    name=master.name,
                    surname=master.surname,
                    phone=master.phone,
                )
            )

        return masters

    def get_master(self, master_id: int) -> MasterInfoWithIdSchema | None:
        master = self.repository.get_object(id=master_id)

        if not master:
            return None

        return MasterInfoWithIdSchema(
            id=master.id,
            name=master.name,
            surname=master.surname,
            phone=master.phone,
        )

    def update_master(
            self,
            master_id: int,
            master_info: MasterUpdateSchema
    ) -> tuple[status, str | MasterInfoSchema]:

        master = self.repository.get_object(id=master_id)
        if not master:
            return status.HTTP_404_NOT_FOUND, "Master not found"

        master_info_dict = master_info.model_dump()

        if master_info.phone is not None:
            if not Service.validate_phone(master_info.phone):
                return (
                    status.HTTP_403_FORBIDDEN,
                    "The entered phone number is incorrect."
                )

        if master_info.password is not None:
            if not self.validate_password(master_info.password):
                return (
                    status.HTTP_403_FORBIDDEN,
                    "Small password length."
                )
            pass_hash = self.hash_password.generate_password_hash(
                password=master.password
            )

            master_info_dict["password"] = pass_hash.hash
            master_info_dict["salt"] = pass_hash.salt

        master_info_dict = delete_none_value_from_dict(master_info_dict)
        self.repository.update_object(master_id, **master_info_dict)
        master = self.repository.get_object(id=master_id)

        return status.HTTP_200_OK, MasterInfoSchema(
            name=master.name,
            surname=master.surname,
            phone=master.phone,
        )
