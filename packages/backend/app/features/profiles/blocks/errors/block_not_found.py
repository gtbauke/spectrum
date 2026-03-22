from fastapi import HTTPException, status


class BlockNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="Block not found")
