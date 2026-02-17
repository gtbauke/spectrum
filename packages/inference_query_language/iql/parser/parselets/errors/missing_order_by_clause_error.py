from iql.parser.parselets.errors.base import AbstractParseletError
from iql.utils.span import Span


class MissingOrderByClauseError(AbstractParseletError):
    def __init__(self, span: Span):
        super().__init__(span, "Expected ORDER BY clause after WHERE clause")
