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

    SELECT = "SELECT"
    FROM = "FROM"
    TOP = "TOP"
    WHERE = "WHERE"
    NOT = "NOT"
    ORDER = "ORDER"
    BY = "BY"
    ALL = "ALL"
    AND = "AND"
    OR = "OR"
    PARETO = "PARETO"
    PATTERN = "PATTERN"
    LIKE = "LIKE"
    IS = "IS"

    NUMBER = "NUMBER"
    IDENTIFIER = "IDENTIFIER"

    EOF = "EOF"

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
            case "ALL":
                return TokenKind.ALL
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
