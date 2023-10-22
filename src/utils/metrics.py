from src.postgres.repositories.error import ErrorRepository
from src.postgres.repositories.category import CategoryRepository
from src.postgres.repositories.log_info import LogInfoRepository
from src.postgres.database import session_ctx
from src.schemas.error import ErrorStatus, Error
from src.services.metrics import (
    errors_by_status_total,
    logs_by_error_total,
    logs_by_category_total,
)


def update_metrics(
    error_repo: ErrorRepository | None = None,
    category_repo: CategoryRepository | None = None,
    log_info_repo: LogInfoRepository | None = None,
):
    if error_repo is None or category_repo is None or log_info_repo is None:
        with session_ctx() as session:
            error_repo = ErrorRepository(session)
            category_repo = CategoryRepository(session)
            log_info_repo = LogInfoRepository(session)
            return update_metrics(error_repo, category_repo, log_info_repo)

    categories = category_repo.get_list(0, 100000)
    categories_map = {category.category_uid: category for category in categories}
    errors = error_repo.get_list(0, 100000)
    errors_by_status = {}
    logs_by_error = {}
    logs_by_category = {}
    for error in errors:
        errors_by_status[error.status] = errors_by_status.get(error.status, 0) + 1
        logs_count = log_info_repo.get_log_infos_count_by_error(error.error_uid)
        logs_by_error[error.title] = logs_count
        category = categories_map.get(error.category_uid)
        category_name = category.title if category else "Unknown"
        logs_by_category[category_name] = (
            logs_by_category.get(category_name, 0) + logs_count
        )

    for status, count in errors_by_status.items():
        errors_by_status_total.labels(status=status.value).set(count)

    for error_title, count in logs_by_error.items():
        logs_by_error_total.labels(error=error_title).set(count)

    for category_name, count in logs_by_category.items():
        logs_by_category_total.labels(category=category_name).set(count)
