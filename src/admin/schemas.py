from pydantic import BaseModel


class MasterInfoSchema(BaseModel):
    name: str
    surname: str
    phone: str
    password: str

    class Config:
        from_attributes = True
