from pydantic import BaseModel, Field

from app.db.models.dataset import DatasetStatus


class UpdateDatasetData(BaseModel):
    name: str = Field(..., description="The name of the dataset")

    status: DatasetStatus = Field(..., description="The status of the dataset")
