from fastapi import HTTPException, status


class InvalidCredentials(HTTPException):
    """Raised when the provided credentials are invalid."""

    def __init__(self, detail: str = "Invalid credentials"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)
