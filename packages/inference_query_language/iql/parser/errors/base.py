from iql.utils.span import Span

class QueryParserError(Exception):
    def __init__(self, message: str, span: Span):
        self.message = message
        self.span = span
        super().__init__(f"{message} at {span}")
