from __future__ import annotations
from enum import StrEnum

from iql.parser.ast.base import BaseAstNode, AstNodeKind
from iql.tokenizer.token import TokenKind
from iql.utils.span import Span


class TokenKindConversionException(Exception):
    def __init__(self, token_kind: TokenKind):
        super().__init__(
            f"No binary operator found for token kind {token_kind}")


class BinaryOperator(StrEnum):
    AND = "AND"
    OR = "OR"
    GREATER_OR_EQUAL = ">="
    LESS_OR_EQUAL = "<="
    GREATER = ">"
    LESS = "<"
    EQUAL = "="

    def is_boolean_operator(self) -> bool:
        return self in {BinaryOperator.AND, BinaryOperator.OR}

    @staticmethod
    def from_token_kind(token_kind: TokenKind) -> BinaryOperator:
        mapping: dict[TokenKind, BinaryOperator] = {
            TokenKind.AND: BinaryOperator.AND,
            TokenKind.OR: BinaryOperator.OR,
            TokenKind.GREATER_EQUAL: BinaryOperator.GREATER_OR_EQUAL,
            TokenKind.LESS_EQUAL: BinaryOperator.LESS_OR_EQUAL,
            TokenKind.GREATER: BinaryOperator.GREATER,
            TokenKind.LESS: BinaryOperator.LESS,
            TokenKind.EQUAL: BinaryOperator.EQUAL,
        }

        if token_kind in mapping:
            return mapping[token_kind]

        raise TokenKindConversionException(token_kind)


class BinaryExpression(BaseAstNode):
    def __init__(self, left: BaseAstNode, operator: BinaryOperator, right: BaseAstNode, span: Span):
        self._left = left
        self._operator = operator
        self._right = right
        super().__init__(kind=AstNodeKind.BINARY_EXPRESSION, span=span)

    def to_string(self, indent: int) -> str:
        indent_str = " " * indent
        return f"{indent_str}BinaryExpression(\n" \
            f"{self._left.to_string(indent + 2)},\n" \
            f"{indent_str}  Operator: {self._operator},\n" \
            f"{self._right.to_string(indent + 2)}\n" \
            f"{indent_str})"

    def left(self) -> BaseAstNode:
        return self._left

    def operator(self) -> BinaryOperator:
        return self._operator

    def right(self) -> BaseAstNode:
        return self._right
