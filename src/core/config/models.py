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
class Config:
    db: DBConfig

