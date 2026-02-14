from uuid import UUID

from app.workers.utils.errors.retryable_error import RetryableError


class DatasetNotReadyForTrainingError(RetryableError):
    def __init__(self, dataset_id: UUID):
        self._dataset_id = dataset_id
        super().__init__(
            f"Dataset with ID {dataset_id} is not ready for training.")
