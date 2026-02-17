from abc import ABC, abstractmethod


class BaseService(ABC):
    """
    Base class for all services in the application. This class defines the interface that all services must implement.
    It also provides common functionality that can be shared across all services.
    """

    @abstractmethod
    async def get(self): ...
