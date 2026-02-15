from app.domain.inference.query.parser.parselet import PrefixParselet
from app.domain.inference.query.parser.ast.base import BaseAstNode
from app.domain.inference.query.parser.base import QueryParser
from app.domain.inference.query.tokenizer.token import Token, TokenKind
from app.domain.inference.query.parser.ast.from_clause import FromAstNode
from app.domain.inference.query.parser.ast.top_n import TopNAstNode, ParetoAstNode


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
