from typing import Optional

from core.models.owners.owner_type import OwnerType


class InvalidOwnerAttachment(Exception):
    """Raised when an invalid attachment is made to an owner."""

    def __init__(self, owner_type: OwnerType, received: Optional[OwnerType]):
        self._owner_type = owner_type
        self._received = received

        super().__init__(
            f"Invalid attachment: expected {owner_type}, but received {received}")
