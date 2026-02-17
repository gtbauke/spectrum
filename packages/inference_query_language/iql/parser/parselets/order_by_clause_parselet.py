from iql.parser.parselet import PrefixParselet
from iql.parser.parser import QueryParser
from iql.parser.ast.base import BaseAstNode
from iql.parser.ast.identifier import IdentifierAstNode
from iql.parser.ast.order_by_clause import OrderByClauseAstNode
from iql.tokenizer.token import Token, TokenKind


class OrderByClauseParselet(PrefixParselet):
    def parse(self, parser: QueryParser, token: Token) -> BaseAstNode:
        parser.consume(TokenKind.BY)
        criteria = parser.parse_expression()

        if not isinstance(criteria, IdentifierAstNode):
            raise ValueError(
                f"Expected identifier in ORDER BY clause, but got {criteria.kind}"
            )

        span = token.span.merge(criteria.span)
        return OrderByClauseAstNode(criteria=criteria, span=span)
