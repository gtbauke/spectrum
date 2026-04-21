from iql.utils.span import Span
from .tokenizer_error import AbstractTokenizerError


class UnterminatedStringError(AbstractTokenizerError):
    def __init__(self, span: Span):
        super().__init__(span=span, message="Unterminated string literal")
