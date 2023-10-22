from datetime import datetime
import uuid
from typing import Union

from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from src.schemas.raw_log import RawLog
from ..database import Base


class RawLogModel(Base):
    __tablename__ = "raw_logs"
    raw_log_uid: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    id: Mapped[str] = mapped_column(String, nullable=True)
    created_date: Mapped[datetime] = mapped_column(DateTime(timezone=False))
    description: Mapped[str] = mapped_column(String, nullable=True)


def model_to_entity(model: RawLogModel) -> RawLog:
    return RawLog(
        raw_log_uid=model.raw_log_uid,
        id=model.id,
        created_date=model.created_date,
        description=model.description,
    )


def entity_to_model(entity: RawLog) -> RawLogModel:
    return RawLogModel(
        raw_log_uid=entity.raw_log_uid,
        id=entity.id,
        created_date=entity.created_date,
        description=entity.description,
    )
