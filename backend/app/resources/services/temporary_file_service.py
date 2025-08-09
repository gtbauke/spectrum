from pathlib import Path
from sqlmodel import Session, select
from fastapi import Depends
from typing import BinaryIO
from app.resources.services.file_service import FileService
from app.resources.datasets.models import Dataset
from app.database import get_session
import tempfile

TEMP_FILE_DIR = Path(tempfile.gettempdir()) / "spectrum_datasets"


class TemporaryFileService(FileService):
    """
    Service for handling temporary files.
    This service can be used to manage temporary files that are not meant to be stored permanently.
    """

    def __init__(self):
        super().__init__()

    def on_server_start(self) -> None:
        pass

    def on_server_shutdown(self, session: Session = Depends(get_session)) -> None:
        """
        Deletes all files in the temporary directory on server shutdown.
        If the directory does not exist, it will be created.
        """
        datasets_with_files = session.exec(
            select(Dataset).where(Dataset.dataset_file_path != None)
        ).all()

        in_use_file_paths = [
            dataset.dataset_file_path for dataset in datasets_with_files]
        if TEMP_FILE_DIR.exists():
            for file in TEMP_FILE_DIR.iterdir():
                if file.name not in in_use_file_paths:
                    file.unlink(missing_ok=True)
        else:
            TEMP_FILE_DIR.mkdir(parents=True, exist_ok=True)

    def upload_file(self, file: BinaryIO, destination: str) -> str:
        TEMP_FILE_DIR.mkdir(parents=True, exist_ok=True)

        temp_file_path = TEMP_FILE_DIR / destination
        temp_file_path.parent.mkdir(parents=True, exist_ok=True)

        file_content = file.read()
        temp_file_path.write_bytes(file_content)

        return str(temp_file_path)

    def download_file(self, file_url: Path, destination: str) -> str:
        raise NotImplementedError

    def delete_file(self, file_path: Path) -> None:
        raise NotImplementedError

    def get_file_path(self, file_name: str) -> Path:
        """
        Returns the path to a file with the specified name in the temporary directory.
        If the file does not exist, it will return a new Path object.
        """
        TEMP_FILE_DIR.mkdir(parents=True, exist_ok=True)
        return TEMP_FILE_DIR / file_name
