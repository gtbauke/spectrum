from fastapi import HTTPException, status


class JobVersionNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job Version not found"
        )
