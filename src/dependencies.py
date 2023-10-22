from typing import Annotated

from fastapi import Depends
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

from src.postgres.database import get_session
from src.postgres.repositories.raw_log import RawLogRepository
from src.postgres.repositories.category import CategoryRepository
from src.postgres.repositories.log_info import LogInfoRepository
from src.postgres.repositories.error_notification import ErrorNotificationRepository
from src.postgres.repositories.error import ErrorRepository


def get_raw_log_repository(
    session: Annotated[Session, Depends(get_session)],
) -> RawLogRepository:
    return RawLogRepository(session=session)


def get_category_repository(
    session: Annotated[Session, Depends(get_session)],
) -> CategoryRepository:
    return CategoryRepository(session=session)


def get_log_info_repository(
    session: Annotated[Session, Depends(get_session)],
) -> LogInfoRepository:
    return LogInfoRepository(session=session)


def get_error_repository(
    session: Annotated[Session, Depends(get_session)],
) -> ErrorRepository:
    return ErrorRepository(session=session)


def get_error_notification_repository(
    session: Annotated[Session, Depends(get_session)],
) -> ErrorNotificationRepository:
    return ErrorNotificationRepository(session=session)
