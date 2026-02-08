from pydantic import BaseModel, Field


class BaseQuery(BaseModel):
    query: str = Field(...,
                       description="The query to be executed against the model.")
