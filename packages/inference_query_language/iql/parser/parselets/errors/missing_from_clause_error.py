from iql.parser.parselets.errors.base import AbstractParseletError
from iql.utils.span import Span


class MissingFromClauseError(AbstractParseletError):
    def __init__(self, span: Span):
        super().__init__(span, "FROM clause is required after SELECT clause")
