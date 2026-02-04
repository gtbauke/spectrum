from pydantic import BaseModel, Field


class CreateDatasetRequest(BaseModel):
    name: str = Field(..., description="The name of the dataset")
