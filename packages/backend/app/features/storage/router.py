from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, RedirectResponse
from pathlib import Path

from app.core.config import settings

router = APIRouter()

@router.get("/download/{path:path}")
async def download_file(path: str):
    """Downloads a file from the spectrum data storage."""
    if settings.STORAGE_TYPE == "s3":
        from core.adapters.storage.s3_storage import S3FileStorage

        storage = S3FileStorage(
            bucket=settings.S3_BUCKET,
            region=settings.S3_REGION,
            access_key=settings.S3_ACCESS_KEY,
            secret_key=settings.S3_SECRET_KEY,
            endpoint_url=settings.S3_ENDPOINT_URL,
        )

        try:
            presigned_url = await storage.generate_download_url(path=path)
        except Exception:
            raise HTTPException(status_code=404, detail="File not found")

        return RedirectResponse(url=presigned_url)

    # Local storage
    base_path = Path(settings.FILE_STORAGE_SPECTRUM_DATA_PATH).resolve()
    file_path = (base_path / path).resolve()

    # Security check: ensure the file is within the base path
    if not str(file_path).startswith(str(base_path)):
        raise HTTPException(status_code=403, detail="Access denied")

    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file_path)

