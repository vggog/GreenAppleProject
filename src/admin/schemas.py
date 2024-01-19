from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class MasterInfoSchema(BaseModel):
    name: str
    surname: str
    phone: str

    class Config:
        from_attributes = True


class MasterInfoWithPassword(MasterInfoSchema):
    password: str


class MasterInfoWithIdSchema(MasterInfoSchema):
    id: int


class MasterUpdateSchema(BaseModel):
    """
    Схема с полями, которые можно обновить у мастера.
    """
    name: Optional[str] = None
    surname: Optional[str] = None
    phone: Optional[str] = None
    password: Optional[str] = None


class MasterChangedStatusSchema(BaseModel):
    id: int
    name: str
    surname: str


class StatusChangeRowSchema(BaseModel):
    status: str
    created_at: datetime
    master: MasterChangedStatusSchema

    class Config:
        from_attributes = True


class RepairOrderSchema(BaseModel):
    id: int
    imei: str
    defect: str
    status: str
    phone_model: str
    created_at: datetime
    updated_at: datetime
    customer_full_name: str
    customer_phone_number: str
    note: Optional[str] = None
    status_changes: list[StatusChangeRowSchema]

    class Config:
        from_attributes = True
