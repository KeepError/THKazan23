import uuid
from typing import Annotated
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from src.postgres.repositories.error_notification import ErrorNotificationRepository

from src.postgres.repositories.error import ErrorRepository
from src.postgres.repositories.raw_log import RawLogRepository
from src.postgres.repositories.category import CategoryRepository
from src.postgres.repositories.log_info import LogInfoRepository
from src.dependencies import (
    get_error_notification_repository,
    get_error_repository,
    get_raw_log_repository,
    get_category_repository,
    get_log_info_repository,
)
from src.schemas.raw_log import RawLog
from src.schemas.error_notification import ErrorNotification
from src.schemas.error import Error, ErrorStatus
from src.schemas.routes.dashboard import (
    GetErrorsResponse,
    ErrorInfo,
    ErrorNotificationRequest,
    ErrorMailRequest,
)
from src.schemas.routes.service import AddRawLog
from src.services.mail import send_mail

dashboard_router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@dashboard_router.get("/errors", response_model=GetErrorsResponse)
def get_errors(
    category_repo: Annotated[CategoryRepository, Depends(get_category_repository)],
    log_info_repo: Annotated[LogInfoRepository, Depends(get_log_info_repository)],
    error_repo: Annotated[ErrorRepository, Depends(get_error_repository)],
    raw_log_repo: Annotated[RawLogRepository, Depends(get_raw_log_repository)],
    offset: int = 0,
    limit: int = 100,
):
    errors = error_repo.get_list(offset=offset, limit=limit)
    errors_info = []
    for error in errors:
        category = category_repo.get_by_uid(error.category_uid)
        category_name = category.title if category else None
        min_date = None
        min_date_log_info = log_info_repo.get_min_log_date_by_error(
            error_uid=error.error_uid
        )
        if min_date_log_info is not None:
            min_date_raw_log = raw_log_repo.get_by_uid(min_date_log_info.raw_log_uid)
            if min_date_raw_log is not None:
                min_date = min_date_raw_log.created_date

        logs_count_total = log_info_repo.get_log_infos_count_by_error(
            error_uid=error.error_uid
        )
        logs_count_last_24h = log_info_repo.get_log_infos_count_by_error(
            error_uid=error.error_uid, start_date=datetime.now() - timedelta(days=1)
        )
        logs_count_last_3d = log_info_repo.get_log_infos_count_by_error(
            error_uid=error.error_uid, start_date=datetime.now() - timedelta(days=3)
        )
        logs_count_last_1mo = log_info_repo.get_log_infos_count_by_error(
            error_uid=error.error_uid, start_date=datetime.now() - timedelta(days=30)
        )
        errors_info.append(
            ErrorInfo(
                error_uid=error.error_uid,
                title=error.title,
                category=category_name,
                status=error.status,
                date=min_date,
                logs_count_total=logs_count_total,
                logs_count_last_24h=logs_count_last_24h,
                logs_count_last_3d=logs_count_last_3d,
                logs_count_last_1mo=logs_count_last_1mo,
            )
        )
    return GetErrorsResponse(errors=errors_info, count=error_repo.get_count())


@dashboard_router.get("/errors/{error_uid}", response_model=ErrorInfo)
def get_error(
    category_repo: Annotated[CategoryRepository, Depends(get_category_repository)],
    log_info_repo: Annotated[LogInfoRepository, Depends(get_log_info_repository)],
    error_repo: Annotated[ErrorRepository, Depends(get_error_repository)],
    raw_log_repo: Annotated[RawLogRepository, Depends(get_raw_log_repository)],
    error_uid: uuid.UUID,
):
    error = error_repo.get_by_uid(error_uid)
    if not error:
        raise HTTPException(status_code=404, detail="Error not found")
    category = category_repo.get_by_uid(error.category_uid)
    category_name = category.title if category else None
    min_date = None
    min_date_log_info = log_info_repo.get_min_log_date_by_error(
        error_uid=error.error_uid
    )
    if min_date_log_info is not None:
        min_date_raw_log = raw_log_repo.get_by_uid(min_date_log_info.raw_log_uid)
        if min_date_raw_log is not None:
            min_date = min_date_raw_log.created_date

    logs_count_total = log_info_repo.get_log_infos_count_by_error(
        error_uid=error.error_uid
    )
    logs_count_last_24h = log_info_repo.get_log_infos_count_by_error(
        error_uid=error.error_uid, start_date=datetime.now() - timedelta(days=1)
    )
    logs_count_last_3d = log_info_repo.get_log_infos_count_by_error(
        error_uid=error.error_uid, start_date=datetime.now() - timedelta(days=3)
    )
    logs_count_last_1mo = log_info_repo.get_log_infos_count_by_error(
        error_uid=error.error_uid, start_date=datetime.now() - timedelta(days=30)
    )
    return ErrorInfo(
        error_uid=error.error_uid,
        title=error.title,
        category=category_name,
        status=error.status,
        date=min_date,
        logs_count_total=logs_count_total,
        logs_count_last_24h=logs_count_last_24h,
        logs_count_last_3d=logs_count_last_3d,
        logs_count_last_1mo=logs_count_last_1mo,
    )


@dashboard_router.put("/errors/{error_uid}/status", response_model=Error)
def set_error_status(
    error_repo: Annotated[ErrorRepository, Depends(get_error_repository)],
    error_uid: uuid.UUID,
    status: ErrorStatus,
):
    error = error_repo.set_status(error_uid=error_uid, status=status)
    if not error:
        raise HTTPException(status_code=404, detail="Error not found")
    return error


@dashboard_router.get(
    "/errors/{error_uid}/notification", response_model=ErrorNotification
)
def get_error_notification(
    error_notification_repo: Annotated[
        ErrorNotificationRepository, Depends(get_error_notification_repository)
    ],
    error_uid: uuid.UUID,
):
    error_notification = error_notification_repo.get_by_uid(error_uid)
    if error_notification is None:
        error_notification = error_notification_repo.add(
            ErrorNotification(error_uid=error_uid, appear_text=None)
        )
    return error_notification


@dashboard_router.put(
    "/errors/{error_uid}/notification", response_model=ErrorNotification
)
def update_error_notification(
    error_notification_repo: Annotated[
        ErrorNotificationRepository, Depends(get_error_notification_repository)
    ],
    error_uid: uuid.UUID,
    error_notification_request: ErrorNotificationRequest,
):
    error_notification = error_notification_repo.get_by_uid(error_uid)
    error_notification = error_notification_repo.update(
        ErrorNotification(
            error_uid=error_uid, appear_text=error_notification_request.appear_text
        )
    )
    return error_notification


@dashboard_router.get("/errors/{error_uid}/logs", response_model=list[RawLog])
def get_error_logs(
    log_info_repo: Annotated[LogInfoRepository, Depends(get_log_info_repository)],
    raw_log_repo: Annotated[RawLogRepository, Depends(get_raw_log_repository)],
    error_uid: uuid.UUID,
    offset: int = 0,
    limit: int = 100,
):
    logs_info = log_info_repo.get_log_infos_by_error(
        error_uid=error_uid, offset=offset, limit=limit
    )
    logs = []
    for log_info in logs_info:
        raw_log = raw_log_repo.get_by_uid(log_info.raw_log_uid)
        if raw_log is not None:
            logs.append(raw_log)
    return logs


@dashboard_router.post("/errors/{error_uid}/mail")
def send_error_mail(
    error_repo: Annotated[ErrorRepository, Depends(get_error_repository)],
    error_mail_request: ErrorMailRequest,
    error_uid: uuid.UUID,
):
    send_mail(
        recipients=error_mail_request.recipients,
        subject=error_mail_request.title,
        text=error_mail_request.text,
    )
