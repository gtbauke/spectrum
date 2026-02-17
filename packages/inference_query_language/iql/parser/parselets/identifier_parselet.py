from iql.parser.parselet import PrefixParselet
from iql.parser.ast.base import BaseAstNode
from iql.parser.base import QueryParser
from iql.tokenizer.token import Token
from iql.parser.ast.identifier import IdentifierAstNode


class IdentifierParselet(PrefixParselet):
    def parse(self, parser: QueryParser, token: Token) -> BaseAstNode:
        return IdentifierAstNode(token.lexeme, token.span)
