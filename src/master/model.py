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
    status_changes: Mapped[list["StatusChangedModel"]] = relationship(
        lazy="selectin"
    )

    note: Mapped[Optional[str]]


class StatusChangedModel(BaseModel):
    __tablename__ = "status_changed_table"

    status: Mapped[str]

    master_id: Mapped[int] = mapped_column(ForeignKey("masters.id"))
    master: Mapped["MasterModel"] = relationship(lazy="selectin")

    repair_order_id: Mapped[int] = mapped_column(
        ForeignKey("repair_orders.id")
    )
    repair_order: Mapped["RepairOrderModel"] = relationship(
        back_populates="status_changes"
    )
