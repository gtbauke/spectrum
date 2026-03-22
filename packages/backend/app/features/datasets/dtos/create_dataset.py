from pydantic import BaseModel, Field

class CreateDatasetDto(BaseModel):
    name: str = Field(..., description="The name of the dataset")
    description: str = Field(..., description="The description of the dataset")
