from fastapi import UploadFile

from core.common.file_storage.base import AbstractFileStorage


async def save_upload(
    *,
    file_storage: AbstractFileStorage,
    upload_file: UploadFile,
    destination: str,
) -> str:
    """
    Save an uploaded file to the specified destination using the provided file storage.

    Args:
        file_storage (AbstractFileStorage): The file storage instance to use for saving the file.
        upload_file (UploadFile): The uploaded file to be saved.
        destination (str): The destination path where the file should be saved.

    Returns:
        str: The path where the file was saved.
    """
    try:
        return await file_storage.save(
            content=upload_file.file,
            destination=destination,
        )
    finally:
        await upload_file.close()
