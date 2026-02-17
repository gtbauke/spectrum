from __future__ import annotations

from typing import Optional
from uuid import UUID
from pydantic import Field

from app.domain.base import BaseDomainModel


class DatasetMetadata(BaseDomainModel):
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
