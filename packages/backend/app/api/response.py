from pydantic import BaseModel


class PaginatedResponse[T](BaseModel):
    items: list[T]
    total: int
    page: int
    size: int
    pages: int


class RepositoryPaginatedResponse[T](BaseModel):
    items: list[T]
    total: int
