from uuid import UUID
from app.workers.utils.errors.unretryable_error import UnretryableError


class ModelNotFoundError(UnretryableError):
    def __init__(self, model_id: UUID):
        self._model_id = model_id
        super().__init__(f"Model with ID {model_id} not found.")
