from pydantic import BaseModel

class UpdateDatasetDto(BaseModel):
    name: str | None = None
    description: str | None = None
