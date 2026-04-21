from __future__ import annotations

from enum import StrEnum
from typing import Callable


class IqlType(StrEnum):
    """Types that IQL expressions can evaluate to."""
    INTEGER = "integer"
    FLOAT = "float"
    STRING = "string"
    BOOLEAN = "boolean"
    NUMERIC = "numeric"       # Supertype for INTEGER | FLOAT
    DATAFRAME = "dataframe"
    ANY = "any"

    def accepts(self, other: IqlType) -> bool:
        """Return True if *self* can accept a value of type *other*."""
        if self is IqlType.ANY or other is IqlType.ANY:
            return True

        if self is IqlType.NUMERIC:
            return other in {IqlType.INTEGER, IqlType.FLOAT, IqlType.NUMERIC}

        return self == other


class FunctionParameter:
    """Describes a single parameter of a builtin function."""

    def __init__(
        self,
        name: str,
        expected_type: IqlType,
        *,
        is_variadic: bool = False,
        is_keyword: bool = False,
    ):
        self.name = name
        self.expected_type = expected_type
        self.is_variadic = is_variadic
        self.is_keyword = is_keyword

    def __repr__(self) -> str:
        prefix = "**" if self.is_keyword else ("*" if self.is_variadic else "")
        return f"{prefix}{self.name}: {self.expected_type}"


class FunctionDefinition:
    """Declares the signature and implementation of a builtin IQL function."""

    def __init__(
        self,
        name: str,
        parameters: list[FunctionParameter],
        return_type: IqlType,
        implementation: Callable[..., object] | None = None,
        *,
        description: str = "",
    ):
        self.name = name.upper()
        self.parameters = parameters
        self.return_type = return_type
        self.implementation = implementation
        self.description = description

    def __repr__(self) -> str:
        params = ", ".join(repr(p) for p in self.parameters)
        return f"FunctionDefinition({self.name}({params}) -> {self.return_type})"


class FunctionRegistry:
    """Central catalogue of builtin IQL functions.

    New builtins are registered here so the Analyzer can validate call
    signatures and the Executor can look up implementations.
    """

    def __init__(self) -> None:
        self._functions: dict[str, FunctionDefinition] = {}

    def register(self, definition: FunctionDefinition) -> None:
        self._functions[definition.name] = definition

    def get(self, name: str) -> FunctionDefinition | None:
        return self._functions.get(name.upper())

    def has(self, name: str) -> bool:
        return name.upper() in self._functions

    @property
    def names(self) -> list[str]:
        return list(self._functions.keys())

    def __repr__(self) -> str:
        return f"FunctionRegistry(functions={self.names})"


def create_default_registry() -> FunctionRegistry:
    """Build the registry with all builtin IQL functions."""
    registry = FunctionRegistry()

    # PREDICT(variable = value, ...)
    # The actual implementation is plugged in by the Executor at runtime,
    # but the signature is declared here for validation.
    predict = FunctionDefinition(
        name="PREDICT",
        parameters=[
            FunctionParameter("assignments", IqlType.NUMERIC, is_keyword=True),
        ],
        return_type=IqlType.DATAFRAME,
        description="Evaluate the expression for the given variable assignments.",
    )
    registry.register(predict)

    return registry
