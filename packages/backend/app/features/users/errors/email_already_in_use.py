from fastapi import HTTPException, status


class EmailAlreadyInUse(HTTPException):
    """Raised when the provided email is already in use."""

    def __init__(self, email: str):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST,
                         detail=f"Email '{email}' is already in use")
