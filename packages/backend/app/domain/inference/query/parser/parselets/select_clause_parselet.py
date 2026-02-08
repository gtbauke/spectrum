import logging

from app.domain.inference.query.parser.parselet import PrefixParselet
from app.domain.inference.query.parser.base import QueryParser
from app.domain.inference.query.parser.ast.base import BaseAstNode, AstNodeKind
from app.domain.inference.query.parser.ast.identifier import IdentifierAstNode
from app.domain.inference.query.parser.ast.select import SelectClauseAstNode
from app.domain.inference.query.parser.ast.from_clause import FromAstNode
from app.domain.inference.query.tokenizer.token import Token, TokenKind

from app.domain.inference.query.parser.parselets.from_clause_parselet import FromClauseParselet

logger = logging.getLogger(__name__)


class SelectListElementMustBeIdentifierException(Exception):
    def __init__(self, actual_kind: AstNodeKind):
        super().__init__(
            f"Expected identifier in SELECT list, but got {actual_kind}")


class MissingFromClauseException(Exception):
    def __init__(self):
        super().__init__("FROM clause is required after SELECT clause")


class SelectClauseParselet(PrefixParselet):
    def __init__(self):
        self._from_clause_parselet = FromClauseParselet()

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

        span = token.span.merge(results[-1].span) if results else token.span
        return SelectClauseAstNode(
            columns=identifier_results,
            from_clause=from_clause,
            span=span
        )
