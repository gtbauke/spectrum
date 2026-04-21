from iql.parser.ast.string import StringLiteralAstNode
from iql.parser.base import QueryParser
from iql.parser.parselet import PrefixParselet
from iql.tokenizer.token import Token


class StringLiteralParselet(PrefixParselet):
    def __init__(self) -> None:
        super().__init__()

    def parse(self, parser: QueryParser, token: Token) -> StringLiteralAstNode:
        value = token.lexeme[1:-1]
        return StringLiteralAstNode(value=value, span=token.span)
