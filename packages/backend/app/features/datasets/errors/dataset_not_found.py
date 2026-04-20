from fastapi import HTTPException, status


class DatasetNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND,
                         detail="Dataset not found")
