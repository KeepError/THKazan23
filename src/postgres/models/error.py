from datetime import datetime
import uuid

from sqlalchemy import DateTime, String, Enum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from src.schemas.error import Error, ErrorStatus
from ..database import Base


class ErrorModel(Base):
    __tablename__ = "errors"
    error_uid: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    category_uid: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=True)
    title: Mapped[str] = mapped_column(String(128), nullable=True)
    status: Mapped[Enum] = mapped_column(Enum(ErrorStatus))


def model_to_entity(model: ErrorModel) -> Error:
    return Error(
        error_uid=model.error_uid,
        category_uid=model.category_uid,
        title=model.title,
        status=ErrorStatus(model.status),
    )


def entity_to_model(entity: Error) -> ErrorModel:
    return ErrorModel(
        error_uid=entity.error_uid,
        category_uid=entity.category_uid,
        title=entity.title,
        status=entity.status,
    )
