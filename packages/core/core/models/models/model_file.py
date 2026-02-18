from __future__ import annotations

from uuid import UUID
from pydantic import BaseModel, Field, computed_field


class ModelFile(BaseModel):
    dataset_id: UUID = Field(
        ..., description="The unique identifier of the dataset associated with the model.")

    job_id: UUID = Field(
        ..., description="The unique identifier of the job associated with the model.")

    file_name: str = Field(...,
                           description="The name of the model file, including its extension.")

    scope: str = Field(
        default="datasets", description="The scope of the file, which can be used to categorize or group files within a dataset."
    )

    @computed_field
    @property
    def relative_directory(self) -> str:
        return f"{self.scope}/{self.dataset_id}"

    @computed_field
    @property
    def relative_path(self) -> str:
        return f"{self.relative_directory}/{self.file_name}"

    @classmethod
    def new_model_file(
        cls,
        *,
        dataset_id: UUID,
        job_id: UUID,
    ) -> ModelFile:
        file_name = f"{dataset_id}_{job_id}_model.eggp"

        return cls(
            dataset_id=dataset_id,
            job_id=job_id,
            file_name=file_name
        )
