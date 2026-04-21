from iql.parser.ast.string import StringLiteralAstNode
from iql.parser.base import QueryParser
from iql.parser.parselet import PrefixParselet
from iql.tokenizer.token import Token


class StringLiteralParselet(PrefixParselet):
    def __init__(self) -> None:
        super().__init__()

    def parse(self, parser: QueryParser, token: Token) -> StringLiteralAstNode:
        return StringLiteralAstNode(value=token.lexeme, span=token.span)
