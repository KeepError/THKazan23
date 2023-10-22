import uuid
from typing import Optional

from sqlalchemy.orm.session import Session

from src.schemas.error import Error, ErrorStatus
from ..models.error import ErrorModel, model_to_entity, entity_to_model


class ErrorRepository:
    session: Session

    def __init__(self, session: Session):
        self.session = session

    def get_by_uid(self, error_uid: uuid.UUID) -> Error | None:
        error_model = (
            self.session.query(ErrorModel)
            .filter(ErrorModel.error_uid == error_uid)
            .first()
        )
        if not error_model:
            return None
        return model_to_entity(error_model)

    def get_by_title(self, title: str) -> Error | None:
        error_model = (
            self.session.query(ErrorModel).filter(ErrorModel.title == title).first()
        )
        if not error_model:
            return None
        return model_to_entity(error_model)

    def get_list(self, offset: int, limit: int) -> list[Error]:
        error_models = self.session.query(ErrorModel).offset(offset).limit(limit).all()
        return list(map(model_to_entity, error_models))
    
    def get_count(self) -> int:
        return self.session.query(ErrorModel).count()

    def add(self, error: Error) -> Error:
        error_model = entity_to_model(error)
        self.session.add(error_model)
        self.session.commit()
        return model_to_entity(error_model)
    
    def set_status(self, error_uid: uuid.UUID, status: ErrorStatus) -> Error | None:
        error_model = (
            self.session.query(ErrorModel)
            .filter(ErrorModel.error_uid == error_uid)
            .first()
        )
        if not error_model:
            return None
        error_model.status = status
        self.session.commit()
        return model_to_entity(error_model)

    def get_count_by_status(self, status: ErrorStatus) -> int:
        return (
            self.session.query(ErrorModel).filter(ErrorModel.status == status).count()
        )

    def next_uid(self) -> uuid.UUID:
        return Error.next_id()
