from pydantic import BaseModel, Field
from datetime import datetime, timezone
from uuid import UUID, uuid4


class RootDomainModel(BaseModel):
    pass


class BaseDomainModel(RootDomainModel):
    """
    Base class for all domain models in the application.
    This class provides common functionality that can be shared across all domain models, such as automatic timestamping of created and updated records.
    """

    id: UUID = Field(uuid4(), description="Unique identifier for the model")

    created_at: datetime = Field(default_factory=datetime.now,
                                 description="Timestamp when the model was created")

    updated_at: datetime = Field(default_factory=datetime.now,
                                 description="Timestamp when the model was last updated")


class BaseImmutableDomainModel(RootDomainModel):
    """
    Base class for all immutable domain models in the application.
    This class is intended for models that should not be modified after creation, such as value objects or read-only representations of data.
    """
    id: UUID = Field(uuid4(), description="Unique identifier for the model")

    version: int = Field(1,
                         description="Version number for optimistic concurrency control")

    timestamp: datetime = Field(datetime.now(timezone.utc),
                                description="Timestamp when the model was created")

    is_latest: bool = Field(
        True, description="Indicates if this is the latest version of the model")
