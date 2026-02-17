from iql.parser.ast.base import BaseAstNode
from iql.parser.parselet import PrefixParselet
from iql.parser.base import QueryParser
from iql.tokenizer.token import Token, TokenKind
from iql.parser.ast.number import (
    IntegerLiteralAstNode,
    FloatLiteralAstNode,
)


class ExpectedNumberTokenException(Exception):
    def __init__(self, token: Token):
        message = f"Expected number token, got {token.kind}"
        super().__init__(message)


class NumberParselet(PrefixParselet):
    def parse(self, parser: QueryParser, token: Token) -> BaseAstNode:
        if not token.kind == TokenKind.NUMBER:
            raise ExpectedNumberTokenException(token)

        if "." in token.lexeme:
            value = float(token.lexeme)
            return FloatLiteralAstNode(value, token.span)

        value = int(token.lexeme)
        return IntegerLiteralAstNode(value, token.span)
