from datetime import datetime
import uuid

from pydantic import BaseModel


class RawLog(BaseModel):
    raw_log_uid: uuid.UUID
    id: str
    created_date: datetime
    description: str

    @staticmethod
    def next_id():
        return uuid.uuid4()
