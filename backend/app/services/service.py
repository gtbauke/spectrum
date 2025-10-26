from abc import ABC, abstractmethod


class Service(ABC):
    @abstractmethod
    async def on_server_startup(self):
        pass

    @abstractmethod
    async def on_server_shutdown(self):
        pass
