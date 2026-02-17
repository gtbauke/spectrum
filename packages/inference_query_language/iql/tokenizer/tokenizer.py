import logging

from iql.tokenizer.errors.unexpected_character_error import UnexpectedCharacterError
from iql.tokenizer.token import Token, TokenKind
from iql.utils.span import Span

logger = logging.getLogger(__name__)


class QueryTokenizer:
    def __init__(self, query: str):
        self._start = 0
        self._current = 0
        self._query = query

    def _advance(self) -> str:
        if self._current >= len(self._query):
            return ""

        char = self._query[self._current]
        self._current += 1

        return char

    def _peek(self, offset: int = 0) -> str:
        pos = self._current + offset

        if pos >= len(self._query):
            return ""

        return self._query[pos]

    def _is_at_end(self) -> bool:
        return self._current >= len(self._query)

    def _skip_whitespace(self):
        while not self._is_at_end() and self._peek().isspace():
            self._advance()

    def _matches(self, expected: str) -> bool:
        if self._is_at_end():
            return False

        if self._peek() != expected:
            return False

        self._advance()
        return True

    def _number(self) -> Token:
        while self._peek().isdigit():
            self._advance()

        if self._peek() == ".":
            self._advance()

            while self._peek().isdigit():
                self._advance()

        lexeme = self._query[self._start:self._current]
        return Token(TokenKind.NUMBER, lexeme, Span(self._start, self._current))

    def _identifier_number_or_keyword(self) -> Token:
        if self._peek().isdigit():
            return self._number()

        while self._peek().isalnum():
            self._advance()

        lexeme = self._query[self._start:self._current].upper()
        kind = TokenKind.keyword_or_identifier(lexeme)

        return Token(kind, lexeme, Span(self._start, self._current))

    def _next(self) -> Token:
        self._skip_whitespace()
        self._start = self._current

        current = self._advance()

        if current.isdigit():
            return self._number()

        match current:
            case "=":
                return Token(TokenKind.EQUAL, current, Span(self._start, self._current))
            case ">":
                if self._matches("="):
                    return Token(TokenKind.GREATER_EQUAL, ">=", Span(self._start, self._current))
                else:
                    raise UnexpectedCharacterError(
                        ">", Span(self._start, self._current))
            case "<":
                if self._matches("="):
                    return Token(TokenKind.LESS_EQUAL, "<=", Span(self._start, self._current))
                else:
                    raise UnexpectedCharacterError(
                        "<", Span(self._start, self._current))
            case ",":
                return Token(TokenKind.COMMA, current, Span(self._start, self._current))
            case ";":
                return Token(TokenKind.SEMICOLON, current, Span(self._start, self._current))
            case _:
                return self._identifier_number_or_keyword()

    def tokenize(self) -> list[Token]:
        tokens: list[Token] = []

        while not self._is_at_end():
            token = self._next()
            tokens.append(token)

        tokens.append(Token(TokenKind.EOF, "", Span(
            self._current, self._current)))
        return tokens
