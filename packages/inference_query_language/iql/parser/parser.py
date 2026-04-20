from iql.parser.base import QueryParser
from iql.tokenizer.token import Token, TokenKind
from iql.parser.parselets.identifier_parselet import IdentifierParselet
from iql.parser.parselets.select_clause_parselet import SelectClauseParselet
from iql.parser.parselets.number_parselet import NumberParselet
from iql.parser.parselets.binary_expression_parselet import BinaryExpressionParselet
from iql.parser.precedence import Precedence
from iql.parser.parselets.function_call_parselet import FunctionCallParselet


class InferenceQueryParser(QueryParser):
    def __init__(self, tokens: list[Token]):
        super().__init__(tokens)

        self.register_prefix_parselet(
            TokenKind.IDENTIFIER, IdentifierParselet())

        self.register_prefix_parselet(
            TokenKind.NUMBER, NumberParselet())

        self.register_prefix_parselet(
            TokenKind.SELECT, SelectClauseParselet())

        self.register_prefix_parselet(
            TokenKind.PATTERN, IdentifierParselet())

        self.register_prefix_parselet(
            TokenKind.PREDICT, IdentifierParselet()
        )

        self.register_infix_parselets(
            BinaryExpressionParselet(Precedence.TERM),
            TokenKind.PLUS,
            TokenKind.MINUS
        )

        self.register_infix_parselets(
            BinaryExpressionParselet(Precedence.FACTOR),
            TokenKind.STAR,
            TokenKind.SLASH
        )

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

        self.register_infix_parselet(
            TokenKind.LEFT_PAREN,
            FunctionCallParselet()
        )
