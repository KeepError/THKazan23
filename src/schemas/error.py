from datetime import datetime
import uuid
from enum import Enum

from pydantic import BaseModel


class ErrorStatus(Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"


class Error(BaseModel):
    error_uid: uuid.UUID
    title: str
    category_uid: uuid.UUID
    status: ErrorStatus

    @staticmethod
    def next_id():
        return uuid.uuid4()
