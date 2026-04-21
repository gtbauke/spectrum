from abc import ABC, abstractmethod
from enum import StrEnum

from iql.utils.span import Span


class AstNodeKind(StrEnum):
    SELECT_CLAUSE = "SELECT"
    WHERE_CLAUSE = "WHERE"
    ORDER_CLAUSE = "ORDER"
    IDENTIFIER = "IDENTIFIER"
    STRING_LITERAL = "STRING_LITERAL"
    INTEGER_LITERAL = "INTEGER_LITERAL"
    FLOAT_LITERAL = "FLOAT_LITERAL"
    BINARY_EXPRESSION = "BINARY_EXPRESSION"
    FROM_CLAUSE = "FROM"
    TOP_N_EXPRESSION = "TOP_N_EXPRESSION"
    PARETO_EXPRESSION = "PARETO_EXPRESSION"
    PATTERN_MATCHING_EXPRESSION = "PATTERN_MATCHING_EXPRESSION"
    FUNCTION_CALL = "FUNCTION_CALL"
    ALIAS_CLAUSE = "ALIAS_CLAUSE"
    DISTRIBUTION_EXPRESSION = "DISTRIBUTION_EXPRESSION"


class BaseAstNode(ABC):
    def __init__(self, kind: AstNodeKind, span: Span):
        self._kind = kind
        self._span = span

    @abstractmethod
    def to_string(self, indent: int) -> str: ...

    @property
    def kind(self) -> AstNodeKind:
        return self._kind

    @property
    def span(self) -> Span:
        return self._span
