from iql.utils.span import Span

from .base import AbstractPlannerError


class ModelIsNotAvailableError(AbstractPlannerError):
    def __init__(self, *, span: Span, model_name: str, model_id: str):
        super().__init__(
            span=span, message=f"Model '{model_name}' (ID: {model_id}) is not available.")
