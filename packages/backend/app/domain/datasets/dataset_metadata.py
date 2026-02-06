from __future__ import annotations

from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field


class DatasetMetadata(BaseModel):
    id: UUID = Field(...,
                     description="The unique identifier of the dataset metadata")
    dataset_id: UUID = Field(...,
                             description="The unique identifier of the associated dataset")

    num_rows: Optional[int] = Field(...,
                                    description="The number of rows in the dataset")
    num_features: Optional[int] = Field(...,
                                        description="The number of features in the dataset")
    processing_attempts: int = Field(
        ..., description="The number of processing attempts made on the dataset")
    last_processing_error: Optional[str] = Field(
        None, description="The last processing error encountered, if any"
    )
    created_at: datetime = Field(...,
                                 description="The creation timestamp of the dataset metadata")
    updated_at: datetime = Field(...,
                                 description="The last update timestamp of the dataset metadata")
