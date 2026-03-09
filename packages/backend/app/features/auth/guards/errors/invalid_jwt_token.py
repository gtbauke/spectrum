from fastapi import HTTPException, status


class InvalidJWTToken(HTTPException):
    def __init__(self, detail: str = "Invalid JWT token"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )
