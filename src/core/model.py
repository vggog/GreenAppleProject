from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column


class BaseModel(DeclarativeBase):
    id: Mapped[int] = mapped_column(
        primary_key=True
    )
    created_at: Mapped[DateTime] = mapped_column(
        default=datetime.utcnow()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        default=datetime.utcnow(),
        onupdate=datetime.utcnow()
    )
