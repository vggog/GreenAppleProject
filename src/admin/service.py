from src.core.config import load_config


class Service:
    admin_conf = load_config().admin

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
