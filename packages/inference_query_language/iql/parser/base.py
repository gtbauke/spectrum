from __future__ import annotations

import logging

from abc import ABC
from typing import Callable, Optional

from iql.tokenizer.token import Token, TokenKind
from iql.utils.span import Span
from iql.parser.precedence import Precedence
from iql.parser.ast.base import BaseAstNode
from iql.parser.errors import ExpectedTokenException
from iql.parser.parselet import (
    InfixParselet,
    PrefixParselet,
    InfixParseletNotFoundException,
    PrefixParseletNotFoundException,
)


logger = logging.getLogger(__name__)


class QueryParser(ABC):
    def __init__(self, tokens: list[Token]):
        self._tokens = tokens
        self._current = 0

        self._infix_parselets: dict[TokenKind, InfixParselet] = {}
        self._prefix_parselets: dict[TokenKind, PrefixParselet] = {}

    def register_infix_parselet(self, kind: TokenKind, parselet: InfixParselet):
        self._infix_parselets[kind] = parselet

    def register_infix_parselets(self, parselet: InfixParselet, *kinds: TokenKind):
        for kind in kinds:
            self.register_infix_parselet(kind, parselet)

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

    def do_until_matches[T: BaseAstNode](self, *kinds: TokenKind, func: Callable[[QueryParser], T]) -> list[T]:
        results: list[T] = []

        while True:
            result = func(self)
            results.append(result)

            if self.peek().kind in kinds or self.is_at_end():
                break

        return results

    def parse_comma_separated_list[T: BaseAstNode](self, func: Callable[[QueryParser], T]) -> list[T]:
        """
        Parses a comma-separated list of elements using the provided parsing function.
        The parsing function should consume the necessary tokens for each element and return an AST node.

        Trailing commas are allowed, and the function will stop parsing when it encounters a token that is not a comma or when it reaches the end of the token stream.
        A comma can also be present before the first element, in which case it will be ignored and parsing will continue with the next token.
        """
        results: list[T] = []

        while True:
            if self.peek().kind == TokenKind.COMMA:
                self.advance()
                continue

            if self.is_at_end():
                break

            result = func(self)
            results.append(result)

        return results

    def _get_precedence(self) -> Precedence:
        if self.peek().kind.is_clause_boundary():
            return Precedence.NONE

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
