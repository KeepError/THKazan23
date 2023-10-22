from prometheus_client import start_http_server, Summary
from prometheus_client import Counter, Gauge

errors_by_status_total = Gauge("errors_by_status_total", "errors_by_status_total", ["status"])
logs_by_error_total = Gauge("logs_by_error_total", "logs_by_error_total", ["error"])
logs_by_category_total = Gauge("logs_by_category_total", "logs_by_category_total", ["category"])
