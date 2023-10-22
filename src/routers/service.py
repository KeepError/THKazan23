import uuid
from typing import Annotated

from fastapi import APIRouter, Depends

from src.postgres.repositories.raw_log import RawLogRepository
from src.postgres.repositories.category import CategoryRepository
from src.postgres.repositories.log_info import LogInfoRepository
from src.postgres.repositories.error import ErrorRepository
from src.dependencies import (
    get_raw_log_repository,
    get_category_repository,
    get_log_info_repository,
    get_error_repository,
)
from src.schemas.raw_log import RawLog
from src.schemas.category import Category
from src.schemas.log_info import LogInfo
from src.schemas.error import Error, ErrorStatus
from src.schemas.routes.service import AddRawLog
from src.utils.metrics import update_metrics
from src.services.classifier import LogClassifier

service_router = APIRouter(prefix="/service", tags=["service"])


@service_router.get("", response_model=list[RawLog])
def get_raw_logs(
    raw_log_repo: Annotated[RawLogRepository, Depends(get_raw_log_repository)],
    offset: int = 0,
    limit: int = 100,
):
    return raw_log_repo.get_list(offset=offset, limit=limit)


@service_router.post("", response_model=RawLog)
def add_raw_log(
    raw_log_repo: Annotated[RawLogRepository, Depends(get_raw_log_repository)],
    category_repo: Annotated[CategoryRepository, Depends(get_category_repository)],
    log_info_repo: Annotated[LogInfoRepository, Depends(get_log_info_repository)],
    error_repo: Annotated[ErrorRepository, Depends(get_error_repository)],
    add_raw_log: AddRawLog,
):
    raw_log = RawLog(
        raw_log_uid=raw_log_repo.next_uid(),
        id=add_raw_log.id,
        created_date=add_raw_log.created_date,
        description=add_raw_log.description,
    )
    raw_log = raw_log_repo.add(raw_log)

    classifier = LogClassifier()
    log_info_data = classifier.predict(raw_log.description)

    category = category_repo.get_by_title(log_info_data.cat_name)
    if not category:
        print("Category not found")
        category = category_repo.add(
            Category(
                category_uid=category_repo.next_uid(),
                title=log_info_data.cat_name,
            )
        )

    error = error_repo.get_by_title(log_info_data.log_type)
    if not error:
        error = error_repo.add(
            Error(
                error_uid=error_repo.next_uid(),
                title=log_info_data.log_type,
                category_uid=category.category_uid,
                status=ErrorStatus.NEW,
            )
        )
    
    log_info = log_info_repo.add_log_info(
        LogInfo(
            raw_log_uid=raw_log.raw_log_uid,
            error_uid=error.error_uid,
        )
    )

    return raw_log
