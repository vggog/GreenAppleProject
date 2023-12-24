from typing import Optional

from sqlalchemy.orm import Mapped

from src.core.model import BaseModel


class MasterModel(BaseModel):
    __tablename__ = "masters"

    name: Mapped[str]
    surname: Mapped[str]
    phone: Mapped[str]
    password: Mapped[str]
    salt: Mapped[str]


class RepairOrderModel(BaseModel):
    __tablename__ = "repair_orders"

    customer_full_name: Mapped[str]
    customer_phone_number: Mapped[str]
    phone_model: Mapped[str]
    imei: Mapped[str]
    defect: Mapped[str]
    note: Mapped[Optional[str]]
