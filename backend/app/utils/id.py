from uuid import UUID
from typing import Union

ID = Union[str, UUID]


def cast_to_uuid(value: ID) -> UUID:
    """
    Casts a value to UUID if it is a string representation of a UUID.
    Raises ValueError if the value cannot be cast to UUID.
    """
    if isinstance(value, UUID):
        return value
    try:
        return UUID(value)
    except ValueError as e:
        raise ValueError(f"Invalid UUID value: {value}") from e
