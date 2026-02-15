from uuid import UUID
from app.workers.utils.errors.retryable_error import RetryableError


class ModelHasNoAssociatedJobError(RetryableError):
    def __init__(self, model_id: UUID):
        self._model_id = model_id
        super().__init__(
            f"Model with ID {model_id} does not have an associated job.")
