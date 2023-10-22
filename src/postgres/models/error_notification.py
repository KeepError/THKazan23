from datetime import datetime
import uuid
from typing import Union

from sqlalchemy import ForeignKey, Column, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from src.schemas.error_notification import ErrorNotification
from ..database import Base


class ErrorNotificationModel(Base):
    __tablename__ = "error_notifications"
    error_uid: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("errors.error_uid"), primary_key=True,
    )
    appear_text: Mapped[str] = mapped_column(String, nullable=True)


def model_to_entity(model: ErrorNotificationModel) -> ErrorNotification:
    return ErrorNotification(
        error_uid=model.error_uid,
        appear_text=model.appear_text,
    )


def entity_to_model(entity: ErrorNotification) -> ErrorNotificationModel:
    return ErrorNotificationModel(
        error_uid=entity.error_uid,
        appear_text=entity.appear_text,
    )
