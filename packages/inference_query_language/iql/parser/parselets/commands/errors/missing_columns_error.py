from iql.parser.errors.base import QueryParserError
from iql.utils.span import Span


class MissingColumnsError(QueryParserError):
    def __init__(self, span: Span):
        super().__init__("SELECT command requires at least one column.", span)
