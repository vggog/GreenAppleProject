from dataclasses import dataclass


@dataclass
class DBConfig:
    db: str
    user: str
    password: str
    host: str
    port: str

    @property
    def alchemy_url(self) -> str:
        return (
            "{dialect_driver}"
            "://{username}:{password}@{host}:{port}/{database}"
        ).format(
            dialect_driver="postgresql+psycopg2",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.db,
        )


@dataclass
class Admin:
    username: str
    password: str


@dataclass
class Auth:
    secret_key: str
    algorithm: str
    access_token_operating_time: int
    refresh_token_operating_time: int


@dataclass
class Config:
    db: DBConfig
    admin: Admin
    auth: Auth
