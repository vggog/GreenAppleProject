from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from src.core.model import BaseModel
from src.core.config import load_config


class BaseRepository:
    engine = create_engine(load_config().db.alchemy_url)
    _model: BaseModel = NotImplemented

    def create(self, **kwargs):
        created_object = self._model(**kwargs)

        with Session(self.engine) as session:
            session.add(created_object)
            session.commit()

    def get_all_datas_from_table(self) -> list[_model]:
        """
        Return all objects.
        :return:
        """
        with Session(self.engine) as session:
            return session.query(self._model).all()

    def get_object(self, **kwargs) -> _model:
        with Session(self.engine) as session:
            return session.query(self._model).filter_by(**kwargs).first()
