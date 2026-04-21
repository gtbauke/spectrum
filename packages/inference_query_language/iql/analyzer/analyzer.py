from __future__ import annotations

import logging

from iql.analyzer.errors.semantic import (
    ColumnNotSelectableError,
    InvalidWhereIdentifierError,
    ModelNotFoundError,
    RootNodeNotSelectError,
    UnknownFunctionError,
)
from iql.analyzer.symbol_table import Symbol, SymbolKind, SymbolTable
from iql.errors.collector import IqlErrorCollector
from iql.parser.ast.base import BaseAstNode
from iql.parser.ast.binary_expression import BinaryExpression
from iql.parser.ast.commands.select_command import SelectCommandAstNode
from iql.parser.ast.function_call import FunctionCallAstNode
from iql.parser.ast.identifier import IdentifierAstNode
from iql.registry.function import FunctionRegistry, IqlType
from iql.utils.planner_constants import QUERYABLE_LITERALS


logger = logging.getLogger(__name__)

_ACCEPTED_WHERE_IDENTIFIERS = frozenset({
    "id",
    "size",
    "parameters",
    "cost",
})


class AnalysisContext:
    """Holds contextual data required by the Analyzer to validate a query."""

    def __init__(
        self,
        available_model_names: list[str],
        function_registry: FunctionRegistry,
    ):
        self.available_model_names = [m.lower() for m in available_model_names]
        self.function_registry = function_registry


class AnalysisResult:
    """Outcome of a successful (or partially successful) analysis pass."""

    def __init__(
        self,
        symbol_table: SymbolTable,
        errors: IqlErrorCollector,
        resolved_model_name: str | None,
    ):
        self.symbol_table = symbol_table
        self.errors = errors
        self.resolved_model_name = resolved_model_name

    @property
    def is_valid(self) -> bool:
        return not self.errors.has_errors()


class SemanticAnalyzer:
    """Traverses the AST and performs symbol resolution and type checking.

    The analyzer populates a ``SymbolTable`` and collects all errors into
    an ``IqlErrorCollector`` so the user receives a comprehensive report.
    """

    def __init__(self, context: AnalysisContext):
        self._context = context
        self._symbol_table = SymbolTable()
        self._errors = IqlErrorCollector()
        self._resolved_model: str | None = None

    def analyze(self, root: BaseAstNode) -> AnalysisResult:
        """Run semantic analysis over the given AST root."""
        if not isinstance(root, SelectCommandAstNode):
            self._errors.add(RootNodeNotSelectError(root.span))
            return self._build_result()

        self._analyze_select(root)
        return self._build_result()

    def _analyze_select(self, node: SelectCommandAstNode) -> None:
        for column in node.columns():
            if isinstance(column, FunctionCallAstNode):
                self._analyze_function_call(column)
            elif isinstance(column, IdentifierAstNode):
                self._analyze_selectable_column(column)
            else:
                if hasattr(column, "name"):
                    col_name = column.name()
                    if col_name not in QUERYABLE_LITERALS:
                        self._errors.add(
                            ColumnNotSelectableError(col_name, column.span)
                        )

        model_ident = node.from_model()
        model_name = model_ident.name()

        if model_name in self._context.available_model_names:
            self._resolved_model = model_name
            self._symbol_table.define(
                Symbol(model_name, SymbolKind.MODEL, IqlType.ANY)
            )
        else:
            self._errors.add(
                ModelNotFoundError(model_name, model_ident.span)
            )

        where_clause = node.where()
        if where_clause:
            self._analyze_where_conditions(where_clause.conditions())

    def _analyze_selectable_column(self, node: IdentifierAstNode) -> None:
        col_name = node.name()
        if col_name not in QUERYABLE_LITERALS:
            self._errors.add(
                ColumnNotSelectableError(col_name, node.span)
            )
        else:
            self._symbol_table.define(
                Symbol(col_name, SymbolKind.COLUMN, IqlType.ANY)
            )

    def _analyze_function_call(self, node: FunctionCallAstNode) -> None:
        fn_name = node.function_name.upper()
        definition = self._context.function_registry.get(fn_name)
        if definition is None:
            self._errors.add(
                UnknownFunctionError(fn_name, node.span)
            )
        else:
            self._symbol_table.define(
                Symbol(fn_name, SymbolKind.FUNCTION, definition.return_type)
            )

    def _analyze_where_conditions(self, conditions: list[BaseAstNode]) -> None:
        for condition in conditions:
            if isinstance(condition, BinaryExpression):
                self._validate_where_expression(condition)

    def _validate_where_expression(self, expr: BinaryExpression) -> None:
        left = expr.left()
        right = expr.right()

        if expr.operator().is_boolean_operator():
            if isinstance(left, BinaryExpression):
                self._validate_where_expression(left)
            if isinstance(right, BinaryExpression):
                self._validate_where_expression(right)
            return

        if isinstance(left, IdentifierAstNode):
            if left.name() not in _ACCEPTED_WHERE_IDENTIFIERS:
                self._errors.add(
                    InvalidWhereIdentifierError(left.name(), left.span)
                )

    def _build_result(self) -> AnalysisResult:
        return AnalysisResult(
            symbol_table=self._symbol_table,
            errors=self._errors,
            resolved_model_name=self._resolved_model,
        )
