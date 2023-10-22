from datetime import datetime
import uuid
from typing import Union

from sqlalchemy import ForeignKey, Column, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from src.schemas.log_info import LogInfo
from ..database import Base


class LogInfoModel(Base):
    __tablename__ = "log_infos"
    raw_log_uid: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("raw_logs.raw_log_uid"), primary_key=True
    )
    error_uid: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("errors.error_uid")
    )


def model_to_entity(model: LogInfoModel) -> LogInfo:
    return LogInfo(
        raw_log_uid=model.raw_log_uid,
        error_uid=model.error_uid,
    )


def entity_to_model(entity: LogInfo) -> LogInfoModel:
    return LogInfoModel(
        raw_log_uid=entity.raw_log_uid,
        error_uid=entity.error_uid,
    )
