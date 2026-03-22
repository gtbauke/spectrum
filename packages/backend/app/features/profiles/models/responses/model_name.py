from pydantic import BaseModel


class ModelNameResponse(BaseModel):
    name: str
