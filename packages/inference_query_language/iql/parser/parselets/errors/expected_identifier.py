from iql.utils.span import Span
from .base import AbstractParseletError


class ExpectedIdentifierParseError(AbstractParseletError):
    def __init__(self, message: str, span: Span):
        super().__init__(span, message)
