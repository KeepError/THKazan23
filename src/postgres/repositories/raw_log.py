import uuid
from typing import Optional

from sqlalchemy.orm.session import Session

from src.schemas.raw_log import RawLog
from ..models.raw_log import RawLogModel, model_to_entity, entity_to_model


class RawLogRepository:
    session: Session

    def __init__(self, session: Session):
        self.session = session

    def get_by_uid(self, raw_log_uid: uuid.UUID) -> RawLog | None:
        raw_log_model = self.session.query(RawLogModel).filter(RawLogModel.raw_log_uid == raw_log_uid).first()
        if not raw_log_model:
            return None
        return model_to_entity(raw_log_model)

    def get_list(self, offset: int, limit: int) -> list[RawLog]:
        raw_log_models = (
            self.session.query(RawLogModel).offset(offset).limit(limit).all()
        )
        return list(map(model_to_entity, raw_log_models))

    def add(self, raw_log: RawLog) -> RawLog:
        raw_log_model = entity_to_model(raw_log)
        self.session.add(raw_log_model)
        self.session.commit()
        return model_to_entity(raw_log_model)

    def next_uid(self) -> uuid.UUID:
        return RawLog.next_id()
