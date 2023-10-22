import uuid

from pydantic import BaseModel


class ErrorNotification(BaseModel):
    error_uid: uuid.UUID
    appear_text: str | None

    @staticmethod
    def next_id():
        return uuid.uuid4()
