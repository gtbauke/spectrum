from iql.parser.parselet import InfixParselet
from iql.parser.ast.base import BaseAstNode
from iql.parser.ast.identifier import IdentifierAstNode
from iql.parser.ast.number import NumericLiteralAstNode
from iql.parser.ast.function_call import FunctionCallAstNode, FunctionArgument
from iql.parser.precedence import Precedence
from iql.tokenizer.token import Token, TokenKind
from iql.utils.span import Span
from iql.parser.parselets.errors.expected_identifier import ExpectedIdentifierParseError
from iql.parser.parselets.errors.expected_number import ExpectedNumberParseError
from iql.parser.parselets.errors.unknown_function import UnknownFunctionParseError

import logging

logger = logging.getLogger(__name__)


class FunctionCallParselet(InfixParselet):
    def parse(self, parser, left: BaseAstNode, token: Token) -> BaseAstNode:
        last_token = token

        if not isinstance(left, IdentifierAstNode):
            raise ExpectedIdentifierParseError(
                "Expected function identifier before '('.", left.span)

        function_name = left.name().upper()
        if function_name != "PREDICT":
            raise UnknownFunctionParseError(
                f"Unsupported function call '{function_name}'.", left.span)

        mappings = []

        while not parser.matches(TokenKind.RIGHT_PAREN):
            id_token = parser.consume(TokenKind.IDENTIFIER)
            variable = IdentifierAstNode(id_token.lexeme, id_token.span)

            parser.consume(TokenKind.EQUAL)

            value = parser.parse_expression()
            if not isinstance(value, NumericLiteralAstNode):
                raise ExpectedNumberParseError(
                    "Expected number for variable value in PREDICT mapping.", value.span)

            mappings.append(FunctionArgument(variable, value))

            if not parser.matches(TokenKind.COMMA):
                last_token = parser.consume(TokenKind.RIGHT_PAREN)
                break

        span = Span(left.span.start, last_token.span.end)
        return FunctionCallAstNode(function_name, mappings, span)

    def precedence(self) -> Precedence:
        return Precedence.CALL
