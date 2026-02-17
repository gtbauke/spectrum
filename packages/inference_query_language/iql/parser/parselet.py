from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from iql.tokenizer.token import Token
from iql.parser.ast.base import BaseAstNode
from iql.parser.precedence import Precedence


if TYPE_CHECKING:
    from iql.parser.base import QueryParser


class PrefixParselet(ABC):
    @abstractmethod
    def parse(self, parser: "QueryParser", token: Token) -> BaseAstNode: ...


class PrefixParseletNotFoundException(Exception):
    def __init__(self, token: Token):
        super().__init__(
            f"No prefix parselet found for token of kind {token.kind}")


class InfixParselet(ABC):
    @abstractmethod
    def parse(self, parser: "QueryParser", left: BaseAstNode,
              token: Token) -> BaseAstNode: ...

    @abstractmethod
    def precedence(self) -> Precedence: ...


class InfixParseletNotFoundException(Exception):
    def __init__(self, token: Token):
        super().__init__(
            f"No infix parselet found for token of kind {token.kind}")
