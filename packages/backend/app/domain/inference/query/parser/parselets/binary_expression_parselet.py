import logging

from app.domain.inference.query.parser.parselet import InfixParselet
from app.domain.inference.query.parser.base import QueryParser
from app.domain.inference.query.parser.ast.base import BaseAstNode
from app.domain.inference.query.parser.precedence import Precedence
from app.domain.inference.query.tokenizer.token import Token
from app.domain.inference.query.parser.ast.binary_expression import BinaryExpression, BinaryOperator


logger = logging.getLogger(__name__)


class BinaryExpressionParselet(InfixParselet):
    def __init__(self, precedence: Precedence) -> None:
        super().__init__()
        self._precedence = precedence

    def precedence(self) -> Precedence:
        return self._precedence

    def parse(self, parser: QueryParser, left: BaseAstNode, token: Token) -> BaseAstNode:
        operator = BinaryOperator.from_token_kind(token.kind)
        right = parser.parse_expression(self._precedence)

        span = left.span.merge(right.span)
        return BinaryExpression(left, operator, right, span)
