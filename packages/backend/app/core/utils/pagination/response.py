from typing import Sequence
from pydantic import BaseModel


class PaginatedResponse[T](BaseModel):
    """
    Base model for paginated responses for Repositories and Services
    """

    items: Sequence[T]
    total: int
    pages: int
    page: int
    size: int
