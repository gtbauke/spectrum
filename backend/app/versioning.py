from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from fastapi import Request
from fastapi import Header, HTTPException, Request
from typing import Optional
from enum import Enum


class APIVersion(str, Enum):
    V1 = "v1"

    @classmethod
    def get_latest(cls) -> "APIVersion":
        """Returns the latest API version."""
        return list(cls)[-1]

    @classmethod
    def get_all_versions(cls) -> list["APIVersion"]:
        """Returns all available API versions."""
        return list(cls)

    @classmethod
    def is_valid_version(cls, version: str) -> bool:
        """Check if a version string is valid."""
        return version in [v.value for v in cls]


def get_api_version_from_header(
    api_version: Optional[str] = Header(None, alias="API-Version")
) -> str:
    """
    Extract API version from header.
    Example: API-Version: v1
    """
    if api_version is None:
        return APIVersion.get_latest().value

    if not APIVersion.is_valid_version(api_version):
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported API version: {api_version}. Supported versions: {[v.value for v in APIVersion.get_all_versions()]}"
        )

    return api_version


def get_api_version_from_accept_header(
    accept: Optional[str] = Header(None)
) -> str:
    """
    Extract API version from Accept header.
    Example: Accept: application/vnd.spectrum.v1+json
    """
    if accept is None:
        return APIVersion.get_latest().value

    # Parse vendor-specific media type
    if "application/vnd.spectrum." in accept:
        try:
            version_part = accept.split("application/vnd.spectrum.")[1]
            # Extract version before +json
            version = version_part.split("+")[0]

            if not APIVersion.is_valid_version(version):
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported API version: {version}. Supported versions: {[v.value for v in APIVersion.get_all_versions()]}"
                )

            return version
        except (IndexError, ValueError):
            pass

    return APIVersion.get_latest().value  # Default


def get_api_version_from_query(request: Request) -> str:
    """
    Extract API version from query parameter.
    Example: /api/datasets?version=v1
    """
    version = request.query_params.get(
        "version", APIVersion.get_latest().value)

    if not APIVersion.is_valid_version(version):
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported API version: {version}. Supported versions: {[v.value for v in APIVersion.get_all_versions()]}"
        )

    return version


class APIVersionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        version = None

        if "version" in request.query_params:
            version = request.query_params["version"]
        elif "api-version" in request.headers:
            version = request.headers["api-version"]
        elif "accept" in request.headers:
            accept = request.headers["accept"]
            if "application/vnd.spectrum." in accept:
                try:
                    version = accept.split(
                        "application/vnd.spectrum.")[1].split("+")[0]
                except:
                    pass

        if not version:
            version = APIVersion.get_latest().value

        request.state.api_version = version
        response = await call_next(request)

        response.headers["API-Version"] = version
        return response
