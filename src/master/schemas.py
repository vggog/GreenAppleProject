from typing import Optional
from datetime import datetime

from pydantic import BaseModel

from src.admin.schemas import MasterInfoWithIdSchema


class CreateRepairOrderSchema(BaseModel):
    customer_full_name: str
    customer_phone_number: str
    phone_model: str
    imei: str
    defect: str
    note: Optional[str]


class RepairOrderSchema(CreateRepairOrderSchema):
    id: int
    created_at: datetime
    updated_at: datetime
    master_id: int
    status: str

    class Config:
        from_attributes = True


class AllInfoOfRepairOrderSchema(RepairOrderSchema):
    master: MasterInfoWithIdSchema

    class Config:
        from_attributes = True


class UpdatedRepairOrderSchema(BaseModel):
    status: str