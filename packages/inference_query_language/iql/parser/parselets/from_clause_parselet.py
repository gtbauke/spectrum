from iql.parser.parselet import PrefixParselet
from iql.parser.ast.base import BaseAstNode
from iql.parser.base import QueryParser
from iql.tokenizer.token import Token, TokenKind
from iql.parser.ast.from_clause import FromAstNode
from iql.parser.ast.top_n import TopNAstNode, ParetoAstNode


class ExpectedTopNOrAllException(Exception):
    def __init__(self):
        super().__init__("Expected TOP or ALL after FROM clause")


class FromClauseParselet(PrefixParselet):
    def parse(self, parser: QueryParser, token: Token) -> BaseAstNode:
        next_token = parser.matches_and_return(TokenKind.PARETO)

        if next_token is not None:
            span = token.span.merge(next_token.span)
            source = ParetoAstNode(span)

            return FromAstNode(source, span)

        top_n_token = parser.matches_and_return(TokenKind.TOP)

        if top_n_token is None:
            raise ExpectedTopNOrAllException()

        top_n_expression = parser.parse_expression()

        span = token.span.merge(top_n_expression.span)
        source = TopNAstNode(top_n_expression, span)

        return FromAstNode(source, span)
