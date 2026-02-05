import logging

from uuid import uuid4
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Any, Callable

from app.core.correlation import correlation_id_ctx


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    # -> Any:
    async def dispatch(self, request: Request, call_next: Callable[[Request], Any]):
        cid = request.headers.get("X-Correlation-ID", str(uuid4()))
        token = correlation_id_ctx.set(cid)

        try:
            response = await call_next(request)
        finally:
            correlation_id_ctx.reset(token)

        response.headers["X-Correlation-ID"] = cid
        return response


class CorrelationIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.correlation_id = correlation_id_ctx.get()
        return True
