from datetime import datetime

from pydantic import BaseModel


class RepairOrderSchema(BaseModel):
    status: str
    created_at: datetime
    updated_at: datetime
