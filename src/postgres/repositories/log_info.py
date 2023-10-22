from datetime import datetime
import uuid

from sqlalchemy.orm.session import Session

from src.schemas.log_info import LogInfo
from ..models.log_info import LogInfoModel, model_to_entity, entity_to_model
from ..models.raw_log import RawLogModel


class LogInfoRepository:
    session: Session

    def __init__(self, session: Session):
        self.session = session

    def get_log_infos_by_error(
        self, error_uid: uuid.UUID, offset: int, limit: int
    ) -> list[LogInfo]:
        log_info_models = (
            self.session.query(LogInfoModel)
            .filter(LogInfoModel.error_uid == error_uid)
            .offset(offset)
            .limit(limit)
            .all()
        )
        return list(map(model_to_entity, log_info_models))

    def get_log_infos_count_by_error(
        self, error_uid: uuid.UUID, start_date: datetime | None = None
    ) -> int:
        if start_date is None:
            return (
                self.session.query(LogInfoModel)
                .filter(LogInfoModel.error_uid == error_uid)
                .count()
            )
        return (
            self.session.query(LogInfoModel)
            .filter(LogInfoModel.error_uid == error_uid)
            .join(RawLogModel)
            .filter(RawLogModel.created_date >= start_date)
            .count()
        )

    def get_min_log_date_by_error(self, error_uid: uuid.UUID) -> LogInfo | None:
        log_info = (
            self.session.query(LogInfoModel)
            .filter(LogInfoModel.error_uid == error_uid)
            .join(RawLogModel)
            .order_by(RawLogModel.created_date.asc())
            .first()
        )
        if not log_info:
            return None
        return model_to_entity(log_info)

    def add_log_info(self, log_info: LogInfo) -> LogInfo:
        log_info_model = entity_to_model(log_info)
        self.session.add(log_info_model)
        self.session.commit()
        return model_to_entity(log_info_model)
