from iql.parser.base import QueryParser
from iql.parser.parselet import PrefixParselet
from iql.parser.ast.base import BaseAstNode
from iql.parser.ast.pattern_matching_expression import PatternMatchingExpression
from iql.tokenizer.token import Token, TokenKind


class PatternMatchingExpressionParselet(PrefixParselet):
    def parse(self, parser: QueryParser, token: Token) -> BaseAstNode:
        parser.consume(TokenKind.IS)
        parser.consume(TokenKind.LIKE)

        pattern_expression = parser.parse_expression()
        span = token.span.merge(pattern_expression.span)

        return PatternMatchingExpression(pattern_expression, span)
