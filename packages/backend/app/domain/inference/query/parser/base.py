from __future__ import annotations
from abc import ABC
from typing import Callable, Optional

from app.domain.inference.query.tokenizer.token import Token, TokenKind
from app.domain.inference.query.span import Span
from app.domain.inference.query.parser.precedence import Precedence
from app.domain.inference.query.parser.ast.base import BaseAstNode
from app.domain.inference.query.parser.errors import ExpectedTokenException
from app.domain.inference.query.parser.parselet import (
    InfixParselet,
    PrefixParselet,
    InfixParseletNotFoundException,
    PrefixParseletNotFoundException,
)


class QueryParser(ABC):
    def __init__(self, tokens: list[Token]):
        self._tokens = tokens
        self._current = 0

        self._infix_parselets: dict[TokenKind, InfixParselet] = {}
        self._prefix_parselets: dict[TokenKind, PrefixParselet] = {}

    def register_infix_parselet(self, kind: TokenKind, parselet: InfixParselet):
        self._infix_parselets[kind] = parselet

    def register_prefix_parselet(self, kind: TokenKind, parselet: PrefixParselet):
        self._prefix_parselets[kind] = parselet

    def is_at_end(self) -> bool:
        index_out_of_range = self._current >= len(self._tokens)
        is_eof_token = self._tokens[self._current].kind == TokenKind.EOF

        return index_out_of_range or is_eof_token

    def peek(self) -> Token:
        if self.is_at_end():
            return Token(TokenKind.EOF, "", Span(len(self._tokens), len(self._tokens)))

        return self._tokens[self._current]

    def advance(self) -> Token:
        if not self.is_at_end():
            self._current += 1

        return self._tokens[self._current - 1]

    def matches(self, *kinds: TokenKind) -> bool:
        if self.peek().kind in kinds:
            self.advance()
            return True

        return False

    def matches_and_return(self, *kinds: TokenKind) -> Optional[Token]:
        if self.peek().kind in kinds:
            return self.advance()

        return None

    def consume(self, kind: TokenKind) -> Token:
        if self.peek().kind == kind:
            return self.advance()

        raise ExpectedTokenException(kind, self.peek().kind)

    def consume_optional(self, *kinds: TokenKind) -> Optional[Token]:
        if self.peek().kind in kinds:
            return self.advance()

        return None

    def do_until_matches(self, *kinds: TokenKind, func: Callable[[QueryParser], BaseAstNode]):
        results: list[BaseAstNode] = []

        while True:
            result = func(self)
            results.append(result)

            if self.peek().kind in kinds or self.is_at_end():
                break

        return results

    def _get_precedence(self) -> Precedence:
        infix_parselet = self._infix_parselets.get(self.peek().kind)

        if infix_parselet:
            return infix_parselet.precedence()

        return Precedence.NONE

    def parse_expression(self, precedence: Precedence = Precedence.NONE) -> BaseAstNode:
        token = self.advance()
        prefix_parselet = self._prefix_parselets.get(token.kind)

        if not prefix_parselet:
            raise PrefixParseletNotFoundException(token)

        left = prefix_parselet.parse(self, token)

        while precedence.value < self._get_precedence().value:
            token = self.advance()
            infix_parselet = self._infix_parselets.get(token.kind)

            if not infix_parselet:
                raise InfixParseletNotFoundException(token)

            left = infix_parselet.parse(self, left, token)

        return left
