from app.domain.inference.query.parser.base import QueryParser
from app.domain.inference.query.tokenizer.token import Token, TokenKind
from app.domain.inference.query.parser.parselets.identifier_parselet import IdentifierParselet
from app.domain.inference.query.parser.parselets.select_clause_parselet import SelectClauseParselet
from app.domain.inference.query.parser.parselets.number_parselet import NumberParselet
from app.domain.inference.query.parser.parselets.binary_expression_parselet import BinaryExpressionParselet
from app.domain.inference.query.parser.precedence import Precedence


class InferenceQueryParser(QueryParser):
    def __init__(self, tokens: list[Token]):
        super().__init__(tokens)

        self.register_prefix_parselet(
            TokenKind.IDENTIFIER, IdentifierParselet())

        self.register_prefix_parselet(
            TokenKind.NUMBER, NumberParselet())

        self.register_prefix_parselet(
            TokenKind.SELECT, SelectClauseParselet())

        self.register_infix_parselet(
            TokenKind.EQUAL,
            BinaryExpressionParselet(Precedence.EQUALITY))

        self.register_infix_parselet(
            TokenKind.GREATER_EQUAL,
            BinaryExpressionParselet(Precedence.COMPARISON))

        self.register_infix_parselet(
            TokenKind.LESS_EQUAL,
            BinaryExpressionParselet(Precedence.COMPARISON))

        self.register_infix_parselet(
            TokenKind.GREATER,
            BinaryExpressionParselet(Precedence.COMPARISON))

        self.register_infix_parselet(
            TokenKind.LESS,
            BinaryExpressionParselet(Precedence.COMPARISON))

        self.register_infix_parselet(
            TokenKind.AND,
            BinaryExpressionParselet(Precedence.AND))

        self.register_infix_parselet(
            TokenKind.OR,
            BinaryExpressionParselet(Precedence.OR))
