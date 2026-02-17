from pydantic import BaseModel, Field
from fastapi import UploadFile


class CreateDatasetData(BaseModel):
    name: str = Field(..., description="The name of the dataset")

    file: UploadFile = Field(...,
                             description="The file containing the dataset")
