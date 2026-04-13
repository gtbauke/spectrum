from iql.parser.parselet import PrefixParselet
from iql.parser.ast.base import BaseAstNode
from iql.parser.base import QueryParser
from iql.tokenizer.token import Token, TokenKind
from iql.parser.ast.where import WhereAstNode


class WhereParselet(PrefixParselet):
    def _parse_condition_element(self, parser: QueryParser) -> BaseAstNode:
        condition = parser.parse_expression()

        return condition

    def parse(self, parser: QueryParser, token: Token) -> BaseAstNode:
        conditions = parser.do_until_matches(
            TokenKind.ORDER,
            TokenKind.PATTERN,
            TokenKind.AT,
            TokenKind.LIMIT,
            TokenKind.EOF,
            func=self._parse_condition_element
        )

        span = token.span.merge(
            conditions[-1].span) if conditions else token.span

        return WhereAstNode(
            conditions=conditions,
            span=span
        )
