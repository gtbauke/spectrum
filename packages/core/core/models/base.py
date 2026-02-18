from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID


class BaseDomainModel(BaseModel):
    """
    Base class for all domain models in the application.
    This class provides common functionality that can be shared across all domain models, such as automatic timestamping of created and updated records.
    """

    id: UUID = Field(..., description="Unique identifier for the model")

    created_at: datetime = Field(...,
                                 description="Timestamp when the model was created")

    updated_at: datetime = Field(...,
                                 description="Timestamp when the model was last updated")
