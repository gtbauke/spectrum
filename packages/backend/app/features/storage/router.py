from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path

from app.core.config import settings

router = APIRouter()


@router.get("/download/{path:path}")
async def get_download_url(path: str):
    """Returns a download URL for the requested file."""
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

        return {"url": presigned_url}

    # Local storage: return a URL pointing to the local file-serving endpoint
    base_path = Path(settings.FILE_STORAGE_SPECTRUM_DATA_PATH).resolve()
    file_path = (base_path / path).resolve()

    if not str(file_path).startswith(str(base_path)):
        raise HTTPException(status_code=403, detail="Access denied")

    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")

    base_url = (settings.STORAGE_BASE_URL or "").rstrip("/")
    return {"url": f"{base_url}/storage/file/{path}"}


@router.get("/file/{path:path}")
async def serve_local_file(path: str):
    """Serves a file directly from local storage."""
    base_path = Path(settings.FILE_STORAGE_SPECTRUM_DATA_PATH).resolve()
    file_path = (base_path / path).resolve()

    if not str(file_path).startswith(str(base_path)):
        raise HTTPException(status_code=403, detail="Access denied")

    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file_path)

