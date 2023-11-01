from src.core.service import BaseService
from src.master.repository import Repository
from starlette import status
from src.core.authorization import Authorization
from src.core.password import Password
from src.master.model import MasterModel


class Servise(BaseService):
    repository = Repository()
    auth = Authorization()
    password = Password()

    def get_master(self, phone: str, password: str) -> tuple[status, str | MasterModel]:
        master: MasterModel = self.repository.get_object(phone=phone)
        if not master:
            return status.HTTP_404_NOT_FOUND, 'master not found'

        if not self.password.check_password(password, master.salt, master.password):
            return status.HTTP_403_FORBIDDEN, 'password is not a correct!'
        return status.HTTP_200_OK, master
