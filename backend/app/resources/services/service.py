from abc import ABC, abstractmethod
from sqlmodel import Session
from fastapi import Depends
from app.database import get_session


class Service(ABC):
    @abstractmethod
    def on_server_start(self):
        """
        This method should be implemented to handle any initialization tasks when the server starts.
        """
        pass

    @abstractmethod
    def on_server_shutdown(self, session: Session = Depends(get_session)):
        """
        This method should be implemented to handle any cleanup tasks when the server is shutting down.
        """
        pass
