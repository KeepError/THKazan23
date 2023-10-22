from datetime import datetime
import uuid

from pydantic import BaseModel

from src.schemas.error import ErrorStatus

class ErrorInfo(BaseModel):
        error_uid: uuid.UUID
        title: str
        category: str | None
        status: ErrorStatus
        date: datetime | None
        logs_count_total: int
        logs_count_last_24h: int
        logs_count_last_3d: int
        logs_count_last_1mo: int


class GetErrorsResponse(BaseModel):
    errors: list[ErrorInfo]
    count: int


class ErrorNotificationRequest(BaseModel):
    appear_text: str | None


class ErrorMailRequest(BaseModel):
    recipients: list[str]
    title: str
    text: str
