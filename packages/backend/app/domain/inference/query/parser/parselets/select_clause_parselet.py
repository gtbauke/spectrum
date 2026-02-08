import logging

from app.domain.inference.query.parser.parselet import PrefixParselet
from app.domain.inference.query.parser.base import QueryParser
from app.domain.inference.query.parser.ast.base import BaseAstNode, AstNodeKind
from app.domain.inference.query.parser.ast.identifier import IdentifierAstNode
from app.domain.inference.query.parser.ast.select import SelectClauseAstNode
from app.domain.inference.query.parser.ast.from_clause import FromAstNode
from app.domain.inference.query.parser.ast.where import WhereAstNode
from app.domain.inference.query.tokenizer.token import Token, TokenKind

from app.domain.inference.query.parser.parselets.from_clause_parselet import FromClauseParselet
from app.domain.inference.query.parser.parselets.where_parselet import WhereParselet

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

        if not isinstance(where_clause, WhereAstNode):
            raise MissingWhereClauseException()

        span = token.span.merge(
            from_clause.span if not where_clause
            else where_clause.span
        )

        return SelectClauseAstNode(
            columns=identifier_results,
            from_clause=from_clause,
            where_clause=where_clause,
            span=span
        )
