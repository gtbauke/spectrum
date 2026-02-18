from enum import StrEnum


class TaskInfraLookup(StrEnum):
    MAIN_EXCHANGE = "tasks.direct"
    RETRY_EXCHANGE = "tasks.retry"
    DLX_EXCHANGE = "tasks.dlx"

    DLQ_QUEUE = "tasks.dlq"

    DATASET_PROCESSING = "dataset.processing"
    DATASET_PROCESSING_RETRY = "dataset.processing.retry"

    DATASET_PROCESSING_RETRY_1 = "dataset.processing.retry.1"
    DATASET_PROCESSING_RETRY_2 = "dataset.processing.retry.2"
    DATASET_PROCESSING_RETRY_3 = "dataset.processing.retry.3"
    DATASET_PROCESSING_RETRY_4 = "dataset.processing.retry.4"
    DATASET_PROCESSING_RETRY_5 = "dataset.processing.retry.5"

    MODEL_TRAINING = "model.training"
    MODEL_TRAINING_RETRY = "model.training.retry"

    MODEL_TRAINING_RETRY_1 = "model.training.retry.1"
    MODEL_TRAINING_RETRY_2 = "model.training.retry.2"
    MODEL_TRAINING_RETRY_3 = "model.training.retry.3"
    MODEL_TRAINING_RETRY_4 = "model.training.retry.4"
    MODEL_TRAINING_RETRY_5 = "model.training.retry.5"
