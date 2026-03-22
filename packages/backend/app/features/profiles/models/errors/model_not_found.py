from fastapi import HTTPException, status

class ModelNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Model not found",
        )
