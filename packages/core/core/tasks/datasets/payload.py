from uuid import UUID
from pydantic import BaseModel, Field


class DatasetProcessTaskPayload(BaseModel):
    dataset_id: UUID = Field(...,
                             description="The ID of the dataset to process")

    model_config = {
        "from_attributes": True,
    }
