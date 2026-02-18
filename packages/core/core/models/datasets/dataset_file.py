from __future__ import annotations

from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field, computed_field


class DatasetFile(BaseModel):
    dataset_id: UUID = Field(
        ..., description="The unique identifier of the dataset to which the file belongs.")

    file_name: str = Field(...,
                           description="The name of the file, including its extension.")

    scope: str = Field(
        default="datasets", description="The scope of the file, which can be used to categorize or group files within a dataset.")

    @computed_field
    @property
    def relative_directory(self) -> str:
        return f"{self.scope}/{self.dataset_id}"

    @computed_field
    @property
    def relative_path(self) -> str:
        return f"{self.relative_directory}/{self.file_name}"

    @classmethod
    def new_raw_file(
        cls,
        *,
        dataset_id: UUID,
        original_file_name: str,
        now: Optional[datetime] = None,
    ) -> DatasetFile:
        now = now or datetime.now()
        timestamp = int(now.timestamp())

        return cls(
            dataset_id=dataset_id,
            file_name=f"{timestamp}_{original_file_name}",
        )
