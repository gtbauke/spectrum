from enum import StrEnum


class TaskInfraLookup(StrEnum):
    MAIN_EXCHANGE = "tasks.direct"
    RETRY_EXCHANGE = "tasks.retry"
    DLX_EXCHANGE = "tasks.dlx"

    DLQ_QUEUE = "tasks.dlq"
