from abc import ABC

from iql.utils.span import Span


class AbstractInferenceQueryLanguageError(Exception, ABC):
    """Base class for all Inference Query Language errors."""

    def __init__(self, span: Span, message: str):
        self.span = span
        super().__init__(message)
