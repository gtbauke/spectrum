from uuid import UUID, uuid4
from datetime import datetime


class DatasetMetadata:
    def __init__(
        self,
        dataset_id: UUID,
        num_rows: int,
        num_features: int,
        processing_attempts: int,
        last_processing_error: str | None,
        id: UUID | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ):
        self.id = id if id is not None else uuid4()
        self.dataset_id = dataset_id
        self.num_rows = num_rows
        self.num_features = num_features
        self.processing_attempts = processing_attempts
        self.last_processing_error = last_processing_error
        self.created_at = created_at if created_at is not None else datetime.now()
        self.updated_at = updated_at if updated_at is not None else datetime.now()
