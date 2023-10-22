from datetime import datetime
import uuid

from pydantic import BaseModel


class LogInfo(BaseModel):
    raw_log_uid: uuid.UUID
    error_uid: uuid.UUID

    @staticmethod
    def next_id():
        return uuid.uuid4()
