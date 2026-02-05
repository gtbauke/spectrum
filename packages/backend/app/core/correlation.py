import contextvars
import uuid

correlation_id_ctx = contextvars.ContextVar(
    "correlation_id",
    default="",
)


def get_correlation_id() -> str:
    cid = correlation_id_ctx.get()
    if cid == "":
        cid = str(uuid.uuid4())
        correlation_id_ctx.set(cid)
    return cid


def set_correlation_id(value: str | None) -> None:
    if value is None:
        value = str(uuid.uuid4())
    correlation_id_ctx.set(value)
