from __future__ import annotations
from enum import StrEnum

from iql.utils.span import Span


class TokenKind(StrEnum):
    PLUS = "PLUS"
    MINUS = "MINUS"
    STAR = "STAR"
    SLASH = "SLASH"

    EQUAL = "EQUAL"
    GREATER_EQUAL = "GREATER_EQUAL"
    LESS_EQUAL = "LESS_EQUAL"
    GREATER = "GREATER"
    LESS = "LESS"
    COMMA = "COMMA"
    SEMICOLON = "SEMICOLON"
    LEFT_PAREN = "LEFT_PAREN"
    RIGHT_PAREN = "RIGHT_PAREN"

    SELECT = "SELECT"
    FROM = "FROM"
    TOP = "TOP"
    WHERE = "WHERE"
    NOT = "NOT"
    ORDER = "ORDER"
    BY = "BY"
    AND = "AND"
    OR = "OR"
    PARETO = "PARETO"
    PATTERN = "PATTERN"
    LIKE = "LIKE"
    IS = "IS"
    DISTRIBUTION = "DISTRIBUTION"
    AT = "AT"
    LEAST = "LEAST"
    LIMIT = "LIMIT"
    INSERT = "INSERT"
    PLOT = "PLOT"

    NUMBER = "NUMBER"
    IDENTIFIER = "IDENTIFIER"

    EOF = "EOF"

    def is_clause_boundary(self) -> bool:
        return self in {
            TokenKind.SELECT,
            TokenKind.FROM,
            TokenKind.WHERE,
            TokenKind.ORDER,
            TokenKind.PATTERN,
            TokenKind.AT,
            TokenKind.LIMIT,
            TokenKind.DISTRIBUTION,
            TokenKind.INSERT,
            TokenKind.PLOT,
        }

    @staticmethod
    def keyword_or_identifier(lexeme: str) -> TokenKind:
        match lexeme.upper():
            case "SELECT":
                return TokenKind.SELECT
            case "FROM":
                return TokenKind.FROM
            case "TOP":
                return TokenKind.TOP
            case "WHERE":
                return TokenKind.WHERE
            case "NOT":
                return TokenKind.NOT
            case "ORDER":
                return TokenKind.ORDER
            case "BY":
                return TokenKind.BY
            case "AND":
                return TokenKind.AND
            case "OR":
                return TokenKind.OR
            case "PARETO":
                return TokenKind.PARETO
            case "PATTERN":
                return TokenKind.PATTERN
            case "LIKE":
                return TokenKind.LIKE
            case "IS":
                return TokenKind.IS
            case "DISTRIBUTION":
                return TokenKind.DISTRIBUTION
            case "AT":
                return TokenKind.AT
            case "LEAST":
                return TokenKind.LEAST
            case "LIMIT":
                return TokenKind.LIMIT
            case "INSERT":
                return TokenKind.INSERT
            case "PLOT":
                return TokenKind.PLOT
            case _:
                return TokenKind.IDENTIFIER


class Token:
    def __init__(self, kind: TokenKind, lexeme: str, span: Span):
        self._kind = kind
        self._lexeme = lexeme
        self._span = span

    @property
    def kind(self) -> TokenKind:
        return self._kind

    @property
    def lexeme(self) -> str:
        return self._lexeme

    @property
    def span(self) -> Span:
        return self._span
