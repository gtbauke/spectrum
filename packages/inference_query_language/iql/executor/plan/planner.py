from __future__ import annotations

import logging

from iql.analyzer.analyzer import AnalysisResult
from iql.errors.collector import IqlErrorCollector
from iql.executor.plan.nodes import (
    ApplyNode,
    FilterNode,
    LogicalPlan,
    LogicalPlanNode,
    ProjectNode,
    ScanNode,
    SearchMode,
    SearchNode,
)
from iql.parser.ast.base import BaseAstNode
from iql.parser.ast.binary_expression import BinaryExpression
from iql.parser.ast.commands.select_command import SelectCommandAstNode
from iql.parser.ast.function_call import FunctionCallAstNode
from iql.parser.ast.identifier import IdentifierAstNode
from iql.parser.ast.number import IntegerLiteralAstNode, NumericLiteralAstNode
from iql.parser.ast.pattern_matching_expression import PatternMatchingExpression
from iql.parser.ast.top_n import ParetoAstNode, TopNAstNode
from iql.parser.ast.where import WhereAstNode


logger = logging.getLogger(__name__)


class Planner:
    """Transforms a validated AST into a ``LogicalPlan``.

    The planner assumes that semantic analysis has already run and
    that the ``AnalysisResult`` contains a resolved model name (if
    valid). Errors encountered during planning are appended to the
    shared ``IqlErrorCollector``.
    """

    def __init__(
        self,
        root: BaseAstNode,
        analysis: AnalysisResult,
        errors: IqlErrorCollector,
    ):
        self._root = root
        self._analysis = analysis
        self._errors = errors

    def create_plan(self) -> LogicalPlan:
        """Build the logical plan tree from the AST."""
        if not isinstance(self._root, SelectCommandAstNode):
            scan = ScanNode(model_name="<unknown>")
            return LogicalPlan(root=scan)

        return self._plan_select(self._root)

    def _plan_select(self, node: SelectCommandAstNode) -> LogicalPlan:
        model_name = self._analysis.resolved_model_name or node.from_model().name()
        current: LogicalPlanNode = ScanNode(
            model_name=model_name,
            description=f"Bind to model '{model_name}'",
        )

        where_clause = node.where()
        if where_clause:
            conditions = self._build_condition_strings(where_clause)
            if conditions:
                current = FilterNode(
                    conditions=conditions,
                    child=current,
                    description=f"Filter: {', '.join(conditions)}",
                )

        current = self._plan_search(node, current)

        predict_calls = [
            col for col in node.columns()
            if isinstance(col, FunctionCallAstNode)
        ]

        for fn_call in predict_calls:
            arguments: dict[str, float] = {}

            for arg in fn_call.arguments:
                arguments[arg.variable.name()] = float(arg.value.value())

            current = ApplyNode(
                function_name=fn_call.function_name.upper(),
                arguments=arguments,
                child=current,
                description=f"Apply {fn_call.function_name.upper()}({', '.join(f'{k}={v}' for k,
                                                                               v in arguments.items())})",
            )

        columns = self._extract_column_names(node)
        current = ProjectNode(
            columns=columns,
            child=current,
            description=f"Project columns: {', '.join(columns)}",
        )

        return LogicalPlan(root=current)

    def _plan_search(
        self,
        node: SelectCommandAstNode,
        child: LogicalPlanNode,
    ) -> LogicalPlanNode:
        modifier = node.modifier()

        pattern_node = node.pattern_matching_expression()
        pattern_str = self._build_pattern_string(
            pattern_node) if pattern_node else None

        if node.is_distribution():
            n_value = self._resolve_top_n(modifier) if isinstance(
                modifier, TopNAstNode) else 5000
            at_least_node = node.at_least()
            at_least = at_least_node.value() if isinstance(
                at_least_node, IntegerLiteralAstNode) else 10
            limit_node = node.limit()
            limit = limit_node.value() if limit_node else 1000

            return SearchNode(
                mode=SearchMode.DISTRIBUTION,
                n=n_value,
                pattern=pattern_str,
                at_least=at_least,
                limit=limit,
                child=child,
                description=f"Search DISTRIBUTION (fromTop={n_value}, atLeast={at_least}, limit={limit})",
            )

        if isinstance(modifier, TopNAstNode):
            n_value = self._resolve_top_n(modifier)
            return SearchNode(
                mode=SearchMode.TOP_N,
                n=n_value,
                pattern=pattern_str,
                child=child,
                description=f"Search TOP {n_value}",
            )

        if isinstance(modifier, ParetoAstNode):
            return SearchNode(
                mode=SearchMode.PARETO,
                child=child,
                description="Search PARETO front",
            )

        return SearchNode(
            mode=SearchMode.TOP_N,
            n=10,
            pattern=pattern_str,
            child=child,
            description="Search TOP 10 (default)",
        )

    def _build_condition_strings(self, where: WhereAstNode) -> list[str]:
        """Flatten WHERE conditions into Reggression-compatible filter strings."""
        results: list[str] = []

        for condition in where.conditions():
            if isinstance(condition, BinaryExpression):
                condition_str = self._expr_to_string(condition)

                if "AND" in condition_str:
                    parts = condition_str.split("AND")
                    results.extend(p.strip() for p in parts)
                else:
                    results.append(condition_str)

        return results

    def _expr_to_string(self, expr: BinaryExpression) -> str:
        left = expr.left()
        operator = expr.operator()
        right = expr.right()

        if operator.is_boolean_operator():
            left_str = (
                self._expr_to_string(left)
                if isinstance(left, BinaryExpression)
                else str(left.to_string(0)).strip()
            )

            right_str = (
                self._expr_to_string(right)
                if isinstance(right, BinaryExpression)
                else str(right.to_string(0)).strip()
            )

            return f"{left_str} {operator} {right_str}"

        if isinstance(left, IdentifierAstNode):
            right_value = right.to_string(0).strip() if hasattr(
                right, "to_string") else str(right)

            if isinstance(right, NumericLiteralAstNode):
                right_value = right.value()

            return f"{left.name()} {operator} {right_value}"

        return f"{left.to_string(0).strip()} {operator} {right.to_string(0).strip()}"

    def _build_pattern_string(self, pattern_node: PatternMatchingExpression) -> str:
        return pattern_node.pattern.to_string(0).strip()

    def _resolve_top_n(self, modifier: TopNAstNode) -> int:
        value_node = modifier.top_n()
        if value_node is None:
            return 1
        if isinstance(value_node, IntegerLiteralAstNode):
            return value_node.value()
        return 1

    def _extract_column_names(self, node: SelectCommandAstNode) -> list[str]:
        columns: list[str] = []

        for col in node.columns():
            if isinstance(col, FunctionCallAstNode):
                columns.append("prediction")
            elif isinstance(col, IdentifierAstNode):
                columns.append(col.name())
            elif hasattr(col, "name"):
                columns.append(col.name())

        return columns
