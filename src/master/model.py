from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.core.model import BaseModel
from src.core.config import load_config


class MasterModel(BaseModel):
    __tablename__ = "masters"

    name: Mapped[str]
    surname: Mapped[str]
    phone: Mapped[str]
    password: Mapped[str]
    salt: Mapped[str]
    repair_orders: Mapped[list["RepairOrderModel"]] = relationship(
        back_populates="master"
    )


class RepairOrderModel(BaseModel):
    __tablename__ = "repair_orders"

    customer_full_name: Mapped[str]
    customer_phone_number: Mapped[str]
    phone_model: Mapped[str]
    imei: Mapped[str]
    defect: Mapped[str]
    status: Mapped[str] = mapped_column(
        # Статусы заказа находятся в классе ProjectSetUp,
        # модуля src.core.config.models
        default="Принят на ремонт"
    )
    master_id: Mapped[int] = mapped_column(ForeignKey("masters.id"))
    master: Mapped["MasterModel"] = relationship(
        back_populates="repair_orders"
    )
    note: Mapped[Optional[str]]
