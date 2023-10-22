from datetime import datetime

from pydantic import BaseModel


class AddRawLog(BaseModel):
    id: str
    created_date: datetime
    description: str
