from iql.tokenizer.errors.tokenizer_error import AbstractTokenizerError
from iql.utils.span import Span


class UnexpectedCharacterError(AbstractTokenizerError):
    """Raised when an unexpected character is encountered during tokenization."""

    def __init__(self, character: str, span: Span):
        self.character = character
        super().__init__(span, f"Unexpected character '{character}'")
