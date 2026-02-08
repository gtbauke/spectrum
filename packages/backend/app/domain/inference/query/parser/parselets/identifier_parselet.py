from app.domain.inference.query.parser.parselet import PrefixParselet
from app.domain.inference.query.parser.ast.base import BaseAstNode
from app.domain.inference.query.parser.base import QueryParser
from app.domain.inference.query.tokenizer.token import Token
from app.domain.inference.query.parser.ast.identifier import IdentifierAstNode


class IdentifierParselet(PrefixParselet):
    def parse(self, parser: QueryParser, token: Token) -> BaseAstNode:
        return IdentifierAstNode(token.lexeme, token.span)
