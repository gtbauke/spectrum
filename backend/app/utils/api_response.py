from typing import Generic, TypeVar
from pydantic.generics import GenericModel


T = TypeVar('T')


class ApiResponse(GenericModel, Generic[T]):
    """
    A generic API response model that can be used to standardize the structure of API responses.
    """
    data: T
