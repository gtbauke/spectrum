from __future__ import annotations

from enum import StrEnum

from iql.registry.function import IqlType


class SymbolKind(StrEnum):
    """Classifies what an identifier resolves to."""
    COLUMN = "column"
    MODEL = "model"
    FUNCTION = "function"
    VARIABLE = "variable"


class Symbol:
    """A resolved identifier with type and source information."""

    def __init__(
        self,
        name: str,
        kind: SymbolKind,
        iql_type: IqlType,
    ):
        self.name = name
        self.kind = kind
        self.iql_type = iql_type

    def __repr__(self) -> str:
        return f"Symbol({self.name!r}, {self.kind}, {self.iql_type})"


class SymbolTable:
    """Tracks identifier bindings discovered during semantic analysis.

    The table maps lowercase names to their ``Symbol`` metadata so that
    the Analyzer and Planner can verify references and types.
    """

    def __init__(self) -> None:
        self._symbols: dict[str, Symbol] = {}

    def define(self, symbol: Symbol) -> None:
        self._symbols[symbol.name.lower()] = symbol

    def resolve(self, name: str) -> Symbol | None:
        return self._symbols.get(name.lower())

    def has(self, name: str) -> bool:
        return name.lower() in self._symbols

    @property
    def symbols(self) -> list[Symbol]:
        return list(self._symbols.values())

    def __repr__(self) -> str:
        return f"SymbolTable({self._symbols})"
