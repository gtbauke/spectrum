from abc import abstractmethod
from pathlib import Path
from sqlmodel import Session
from fastapi import Depends
from typing import BinaryIO
from app.database import get_session
from app.resources.services.service import Service


class FileService(Service):
    @abstractmethod
    def on_server_start(self) -> None:
        """Method to be called when the server starts."""
        pass

    @abstractmethod
    def on_server_shutdown(self, session: Session = Depends(get_session)) -> None:
        """Method to be called when the server shuts down."""
        pass

    @abstractmethod
    def upload_file(self, file: BinaryIO, destination: str) -> str:
        """Uploads a file to a specified destination."""
        pass

    @abstractmethod
    def download_file(self, file_url: Path, destination: str) -> str:
        """Downloads a file from a specified URL to a local destination."""
        pass

    @abstractmethod
    def delete_file(self, file_path: Path) -> None:
        """Deletes a file at the specified path."""
        pass
