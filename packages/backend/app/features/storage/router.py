from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse
from pathlib import Path
import os

from app.core.config import settings

router = APIRouter()

@router.get("/download/{path:path}")
async def download_file(path: str):
    """Downloads a file from the spectrum data storage."""
    base_path = Path(settings.FILE_STORAGE_SPECTRUM_DATA_PATH).resolve()
    file_path = (base_path / path).resolve()

    # Security check: ensure the file is within the base path
    if not str(file_path).startswith(str(base_path)):
        raise HTTPException(status_code=403, detail="Access denied")

    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file_path)
