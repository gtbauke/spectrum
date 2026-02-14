from uuid import UUID
from app.utils.errors.service_error import ServiceError


class DatasetNotFoundError(ServiceError):
    def __init__(self, dataset_id: UUID) -> None:
        super().__init__(f"Dataset with id {dataset_id} not found")

        self._dataset_id = dataset_id
        self._error_code = 404
