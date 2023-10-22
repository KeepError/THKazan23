import uuid
from typing import Optional

from sqlalchemy.orm.session import Session

from src.schemas.error_notification import ErrorNotification
from ..models.error_notification import ErrorNotificationModel, model_to_entity, entity_to_model


class ErrorNotificationRepository:
    session: Session

    def __init__(self, session: Session):
        self.session = session

    def get_by_uid(self, error_uid: uuid.UUID) -> ErrorNotification | None:
        error_notification_model = (
            self.session.query(ErrorNotificationModel)
            .filter(ErrorNotificationModel.error_uid == error_uid)
            .first()
        )
        if not error_notification_model:
            return None
        return model_to_entity(error_notification_model)
    
    def add(self, error_notification: ErrorNotification) -> ErrorNotification:
        error_notification_model = entity_to_model(error_notification)
        self.session.add(error_notification_model)
        self.session.commit()
        return model_to_entity(error_notification_model)
    
    def update(self, error_notification: ErrorNotification) -> ErrorNotification | None:
        error_notification_model = (
            self.session.query(ErrorNotificationModel)
            .filter(ErrorNotificationModel.error_uid == error_notification.error_uid)
            .first()
        )
        if not error_notification_model:
            return None
        error_notification_model.appear_text = error_notification.appear_text
        self.session.commit()
        return model_to_entity(error_notification_model)
