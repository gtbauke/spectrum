from enum import StrEnum


class TaskInfraLookup(StrEnum):
    MAIN_EXCHANGE = "tasks.direct"
    RETRY_EXCHANGE = "tasks.retry"
    DLX_EXCHANGE = "tasks.dlx"

    DLQ_QUEUE = "tasks.dlq"

    DATASET_PROCESSING = "dataset.processing"
    DATASET_PROCESSING_RETRY = "dataset.processing.retry"

    MODEL_TRAINING = "model.training"
    MODEL_TRAINING_RETRY = "model.training.retry"
