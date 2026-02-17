import logging

from iql.parser.parselet import PrefixParselet
from iql.parser.base import QueryParser
from iql.parser.ast.base import BaseAstNode, AstNodeKind
from iql.parser.ast.identifier import IdentifierAstNode
from iql.parser.ast.select import OrderByClauseAstNode, SelectClauseAstNode
from iql.parser.ast.from_clause import FromAstNode
from iql.parser.ast.where import WhereAstNode
from iql.tokenizer.token import Token, TokenKind

from iql.parser.parselets.from_clause_parselet import FromClauseParselet
from iql.parser.parselets.where_parselet import WhereParselet
from iql.parser.parselets.order_by_clause_parselet import OrderByClauseParselet

logger = logging.getLogger(__name__)


class SelectListElementMustBeIdentifierException(Exception):
    def __init__(self, actual_kind: AstNodeKind):
        super().__init__(
            f"Expected identifier in SELECT list, but got {actual_kind}")


class MissingFromClauseException(Exception):
    def __init__(self):
        super().__init__("FROM clause is required after SELECT clause")


class MissingWhereClauseException(Exception):
    def __init__(self):
        super().__init__("WHERE clause is required after FROM clause")


class SelectClauseParselet(PrefixParselet):
    def __init__(self):
        self._from_clause_parselet = FromClauseParselet()
        self._where_parselet = WhereParselet()
        self._order_by_clause_parselet = OrderByClauseParselet()

    def _parse_select_list_element(self, parser: QueryParser) -> BaseAstNode:
        parser.consume_optional(TokenKind.COMMA)
        expression = parser.parse_expression()

        if expression.kind != AstNodeKind.IDENTIFIER:
            raise SelectListElementMustBeIdentifierException(expression.kind)

        return expression

    def parse(self, parser: QueryParser, token: Token) -> BaseAstNode:
        results = parser.do_until_matches(
            TokenKind.FROM,
            TokenKind.WHERE,
            TokenKind.ORDER,
            TokenKind.EOF,
            func=self._parse_select_list_element,
        )

        identifier_results = [
            result for result in results if isinstance(result, IdentifierAstNode)
        ]

        from_token = parser.matches_and_return(TokenKind.FROM)
        if not from_token:
            raise MissingFromClauseException()

        from_clause = self._from_clause_parselet.parse(parser, from_token)
        if not isinstance(from_clause, FromAstNode):
            raise MissingFromClauseException()

        where_token = parser.matches_and_return(TokenKind.WHERE)
        where_clause = None

        if where_token:
            where_clause = self._where_parselet.parse(parser, where_token)

        if where_clause is not None and not isinstance(where_clause, WhereAstNode):
            raise MissingWhereClauseException()

        order_token = parser.matches_and_return(TokenKind.ORDER)
        order_by_clause = None

        if order_token:
            order_by_clause = self._order_by_clause_parselet.parse(
                parser, order_token)

        if order_by_clause is not None and not isinstance(order_by_clause, OrderByClauseAstNode):
            raise ValueError(
                f"Expected ORDER BY clause, but got {order_by_clause.kind}"
            )

        span = token.span.merge_with_last_non_none(
            from_clause.span,
            where_clause.span if where_clause else None,
            order_by_clause.span if order_by_clause else None
        )

        return SelectClauseAstNode(
            columns=identifier_results,
            from_clause=from_clause,
            where_clause=where_clause,
            order_by_clause=order_by_clause,
            span=span
        )
