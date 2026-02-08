from app.domain.inference.query.parser.parselet import PrefixParselet
from app.domain.inference.query.parser.ast.base import BaseAstNode
from app.domain.inference.query.parser.base import QueryParser
from app.domain.inference.query.tokenizer.token import Token, TokenKind
from app.domain.inference.query.parser.ast.where import WhereAstNode


class WhereParselet(PrefixParselet):
    def _parse_condition_element(self, parser: QueryParser) -> BaseAstNode:
        parser.consume_optional(TokenKind.AND, TokenKind.OR)
        condition = parser.parse_expression()

        return condition

    def parse(self, parser: QueryParser, token: Token) -> BaseAstNode:
        conditions = parser.do_until_matches(
            TokenKind.ORDER,
            TokenKind.EOF,
            func=self._parse_condition_element
        )

        span = token.span.merge(
            conditions[-1].span) if conditions else token.span

        return WhereAstNode(
            conditions=conditions,
            span=span
        )
