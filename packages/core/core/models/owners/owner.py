from pydantic import Field

from core.models.base import BaseImmutableDomainModel
from core.models.owners.owner_type import OwnerType


class Owner(BaseImmutableDomainModel):
    """
    The `Owner` class represents an entity that can own resources within the system. It is designed to be flexible and can represent different types of owners, such as users, teams, or organizations.

    Properties:
    - `owner_type`: An enumeration that specifies the type of owner (e.g., USER, TEAM, ORGANIZATION).
    """
    owner_type: OwnerType = Field(
        ..., description="The type of the owner (e.g., USER, TEAM, ORGANIZATION)")
