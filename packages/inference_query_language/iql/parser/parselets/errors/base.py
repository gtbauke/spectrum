from iql.errors.base import AbstractInferenceQueryLanguageError
from iql.utils.span import Span


class AbstractParseletError(AbstractInferenceQueryLanguageError):
    def __init__(self, span: Span, message: str):
        super().__init__(span, message)
