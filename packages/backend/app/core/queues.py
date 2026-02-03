from pydantic_settings import BaseSettings


class QueueSettings(BaseSettings):
    DATASET_PROCESSING_QUEUE: str = "dataset_processing_queue"
    DATASET_PROCESSING_RETRY_QUEUE: str = "dataset_processing_retry_queue"
    DATASET_PROCESSING_DEAD_LETTER_QUEUE: str = "dataset_processing_dead_letter_queue"

    DATASET_PROCESSING_ROUTING_KEY: str = "dataset.processing"
    DATASET_PROCESSING_RETRY_ROUTING_KEY: str = "dataset.processing.retry"
    DATASET_PROCESSING_DEAD_LETTER_ROUTING_KEY: str = "dataset.processing.dlq"

    DATASET_PROCESSING_EXCHANGE: str = "dataset_processing_exchange"

    MODEL_TRAINING_QUEUE: str = "model_training_queue"
    MODEL_TRAINING_RETRY_QUEUE: str = "model_training_retry_queue"
    MODEL_TRAINING_DEAD_LETTER_QUEUE: str = "model_training_dead_letter_queue"

    MODEL_TRAINING_ROUTING_KEY: str = "model.training"
    MODEL_TRAINING_RETRY_ROUTING_KEY: str = "model.training.retry"
    MODEL_TRAINING_DEAD_LETTER_ROUTING_KEY: str = "model.training.dlq"

    MODEL_TRAINING_EXCHANGE: str = "model_training_exchange"


queue_settings = QueueSettings()
