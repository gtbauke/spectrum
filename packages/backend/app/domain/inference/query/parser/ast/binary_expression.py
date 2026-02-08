from __future__ import annotations
from enum import StrEnum

from app.domain.inference.query.parser.ast.base import BaseAstNode
from app.domain.inference.query.tokenizer.token import TokenKind


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
    def __init__(self, left: BaseAstNode, operator: BinaryOperator, right: BaseAstNode):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f"BinaryExpression(left={self.left}, operator='{self.operator}', right={self.right})"
