from abc import ABC, abstractmethod


class BaseOrchestrator(ABC):
    @abstractmethod
    async def setup(self): ...

    @abstractmethod
    async def run(self): ...
