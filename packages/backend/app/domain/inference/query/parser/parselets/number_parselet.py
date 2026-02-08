from app.domain.inference.query.parser.ast.base import BaseAstNode
from app.domain.inference.query.parser.parselet import PrefixParselet
from app.domain.inference.query.parser.base import QueryParser
from app.domain.inference.query.tokenizer.token import Token, TokenKind
from app.domain.inference.query.parser.ast.number import (
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
