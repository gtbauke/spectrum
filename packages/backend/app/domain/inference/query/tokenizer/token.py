from __future__ import annotations
from enum import StrEnum

from app.domain.inference.query.span import Span


class TokenKind(StrEnum):
    EQUAL = "EQUAL"
    GREATER_EQUAL = "GREATER_EQUAL"
    LESS_EQUAL = "LESS_EQUAL"
    COMMA = "COMMA"

    SELECT = "SELECT"
    FROM = "FROM"
    TOP = "TOP"
    WHERE = "WHERE"
    NOT = "NOT"
    ORDER = "ORDER"
    BY = "BY"
    ALL = "ALL"

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
