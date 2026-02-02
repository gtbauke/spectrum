from uuid import UUID
from pydantic import BaseModel


class DatasetProcessingEvent(BaseModel):
    dataset_id: UUID
    file_path: str
