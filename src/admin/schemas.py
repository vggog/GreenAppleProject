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
