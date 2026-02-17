import logging

from typing import Optional

from iql.parser.ast.pattern_matching_expression import PatternMatchingExpression
from iql.parser.parselet import PrefixParselet
from iql.parser.base import QueryParser
from iql.parser.ast.base import BaseAstNode
from iql.parser.ast.identifier import IdentifierAstNode
from iql.parser.ast.select import OrderByClauseAstNode, SelectClauseAstNode
from iql.parser.ast.from_clause import FromAstNode
from iql.parser.ast.where import WhereAstNode
from iql.tokenizer.token import Token, TokenKind

from iql.parser.parselets.from_clause_parselet import FromClauseParselet
from iql.parser.parselets.where_parselet import WhereParselet
from iql.parser.parselets.order_by_clause_parselet import OrderByClauseParselet
from iql.parser.parselets.pattern_matching_expression_parselet import PatternMatchingExpressionParselet

from iql.parser.parselets.errors.select_clause_invalid_identifier_error import SelectClauseInvalidIdentifierError
from iql.parser.parselets.errors.missing_from_clause_error import MissingFromClauseError
from iql.parser.parselets.errors.missing_pattern_matching_expression_error import MissingPatternMatchingExpressionError
from iql.parser.parselets.errors.missing_order_by_clause_error import MissingOrderByClauseError

logger = logging.getLogger(__name__)


class MissingWhereClauseException(Exception):
    def __init__(self):
        super().__init__("WHERE clause is required after FROM clause")


class SelectClauseParselet(PrefixParselet):
    def __init__(self):
        self._from_clause_parselet = FromClauseParselet()
        self._where_parselet = WhereParselet()
        self._order_by_clause_parselet = OrderByClauseParselet()
        self._pattern_matching_expression_parselet = PatternMatchingExpressionParselet()

    def _parse_select_list_element(self, parser: QueryParser) -> IdentifierAstNode:
        parser.consume_optional(TokenKind.COMMA)
        expression = parser.parse_expression()

        if not isinstance(expression, IdentifierAstNode):
            raise SelectClauseInvalidIdentifierError(expression)

        return expression

    def _parse_from_clause(self, parser: QueryParser) -> FromAstNode:
        from_token = parser.consume(TokenKind.FROM)
        from_clause = self._from_clause_parselet.parse(parser, from_token)

        if not isinstance(from_clause, FromAstNode):
            raise MissingFromClauseError(from_token.span)

        return from_clause

    def _parse_where_clause(self, parser: QueryParser) -> Optional[WhereAstNode]:
        where_token = parser.matches_and_return(TokenKind.WHERE)

        if where_token is None:
            return None

        where_clause = self._where_parselet.parse(parser, where_token)

        if not isinstance(where_clause, WhereAstNode):
            raise MissingWhereClauseException()

        return where_clause

    def _parse_pattern_matching_expression(self, parser: QueryParser) -> Optional[PatternMatchingExpression]:
        pattern_token = parser.matches_and_return(TokenKind.PATTERN)

        if pattern_token is None:
            return None

        pattern_matching_expression = self._pattern_matching_expression_parselet.parse(
            parser, pattern_token)
        if not isinstance(pattern_matching_expression, PatternMatchingExpression):
            raise MissingPatternMatchingExpressionError(pattern_token.span)

        return pattern_matching_expression

    def _parse_order_by_clause(self, parser: QueryParser) -> Optional[OrderByClauseAstNode]:
        order_token = parser.matches_and_return(TokenKind.ORDER)

        if order_token is None:
            return None

        order_by_clause = self._order_by_clause_parselet.parse(
            parser, order_token)

        if not isinstance(order_by_clause, OrderByClauseAstNode):
            raise MissingOrderByClauseError(order_token.span)

        return order_by_clause

    def parse(self, parser: QueryParser, token: Token) -> BaseAstNode:
        results = parser.do_until_matches(
            TokenKind.FROM,
            TokenKind.WHERE,
            TokenKind.ORDER,
            TokenKind.EOF,

            func=self._parse_select_list_element,
        )

        from_clause = self._parse_from_clause(parser)
        where_clause = self._parse_where_clause(parser)

        pattern_matching_expression = self._parse_pattern_matching_expression(
            parser)

        order_by_clause = self._parse_order_by_clause(parser)

        span = token.span.merge_with_last_non_none(
            from_clause.span,
            where_clause.span if where_clause else None,
            pattern_matching_expression.span if pattern_matching_expression else None,
            order_by_clause.span if order_by_clause else None
        )

        return SelectClauseAstNode(
            columns=results,
            from_clause=from_clause,
            where_clause=where_clause,
            order_by_clause=order_by_clause,
            pattern_matching_expression=pattern_matching_expression,
            span=span
        )
