from typing import Optional

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
