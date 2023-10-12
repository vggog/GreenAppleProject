from sqlalchemy.orm import Mapped

from src.core.model import BaseModel


class MasterModel(BaseModel):
    __tablename__ = "masters"

    name: Mapped[str]
    surname: Mapped[str]
