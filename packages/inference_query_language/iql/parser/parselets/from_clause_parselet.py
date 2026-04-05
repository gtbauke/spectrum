from iql.parser.ast.identifier import IdentifierAstNode
from iql.parser.parselet import PrefixParselet
from iql.parser.ast.base import BaseAstNode
from iql.parser.base import QueryParser
from iql.tokenizer.token import Token, TokenKind
from iql.parser.ast.from_clause import FromAstNode


class ExpectedIdentifierException(Exception):
    def __init__(self):
        super().__init__("Expected identifier (model name or ID) after FROM clause")


class FromClauseParselet(PrefixParselet):
    def parse(self, parser: QueryParser, token: Token) -> BaseAstNode:
        identifier = parser.parse_expression()

        if not isinstance(identifier, IdentifierAstNode):
            raise ExpectedIdentifierException()

        # We allow identifiers or potentially strings in the future,
        # but for now we consume whatever expression is there as a identifier
        span = token.span.merge(identifier.span)
        return FromAstNode(identifier, span)
