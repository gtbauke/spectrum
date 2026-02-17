from iql.parser.parselets.errors.base import AbstractParseletError
from iql.utils.span import Span


class MissingPatternMatchingExpressionError(AbstractParseletError):
    def __init__(self, span: Span):
        super().__init__(span, "Expected pattern matching expression after PATTERN keyword")
