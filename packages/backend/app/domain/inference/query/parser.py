from app.domain.inference.query.token import Token, TokenKind
from app.domain.inference.query.span import Span


class QueryParser:
    def __init__(self, tokens: list[Token]):
        self._tokens = tokens
        self._current = 0

    def _is_at_end(self) -> bool:
        return self._current >= len(self._tokens)

    def _peek(self) -> Token:
        if self._is_at_end():
            return Token(TokenKind.EOF, "", Span(len(self._tokens), len(self._tokens)))

        return self._tokens[self._current]

    def _advance(self) -> Token:
        if not self._is_at_end():
            self._current += 1

        return self._tokens[self._current - 1]

    def _matches(self, *kinds: TokenKind) -> bool:
        if self._peek().kind in kinds:
            self._advance()
            return True

        return False

    def _consume(self, kind: TokenKind) -> Token:
        if self._peek().kind == kind:
            return self._advance()

        raise Exception(
            f"Expected token of kind {kind}, but got {self._peek().kind}")
