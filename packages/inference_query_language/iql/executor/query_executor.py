import logging

from pandas import DataFrame
from reggression import Reggression  # type: ignore

from iql.parser.ast.where import WhereAstNode
from iql.parser.base import BaseAstNode
from iql.parser.ast.base import AstNodeKind
from iql.parser.ast.select import IdentifierAstNode, SelectClauseAstNode
from iql.executor.errors.root_expression_should_be_select_clause_error import (
    RootExpressionShouldBeSelectClauseError,
)
from iql.parser.ast.top_n import TopNAstNode
from iql.parser.ast.number import IntegerLiteralAstNode, NumericLiteralAstNode
from iql.parser.ast.binary_expression import BinaryExpression
from iql.executor.errors.column_is_not_selectable_error import ColumnIsNotSelectableError
from iql.utils.result import InferenceResultList, InferenceResult


logger = logging.getLogger(__name__)


class QueryExecutor:
    _QUERYABLE_LITERALS = (
        "id",
        "expression",
        "dl",
        "fitness",
        "latex",
        "numpy",
        "parameters",
        "size",
    )

    def __init__(self, root_node: BaseAstNode, reggression: Reggression):
        self._root_node = root_node
        self._reggression = reggression

    def _calculate_node_value(self, node: BaseAstNode):
        logger.info(f"Calculating value for node: {node.to_string(0)}")

        if isinstance(node, IntegerLiteralAstNode):
            return node.value()

        if isinstance(node, BinaryExpression):
            raise NotImplementedError(
                "Binary expression evaluation is not implemented yet. (Arithmetic operations are not supported yet)")

    def _calculate_top_n(self, top_n_node: TopNAstNode) -> int:
        value = top_n_node.top_n()
        if not value:
            return 1

        n_value = self._calculate_node_value(value)

        logger.info(f"Calculated TOP N value: {n_value}")

        if not isinstance(n_value, int):
            raise ValueError("Top N value must be an integer")

        return n_value

    def _get_condition_string(self, condition: BinaryExpression) -> str:
        left = condition.left()
        operator = condition.operator()
        right = condition.right()

        if not operator.is_boolean_operator() \
                and not isinstance(left, IdentifierAstNode) \
                and not isinstance(right, NumericLiteralAstNode):
            raise ValueError(
                "Only simple binary expressions with identifiers and numeric literals are supported in WHERE clause")

        if operator.is_boolean_operator():
            left_str = self._get_condition_string(left) \
                if isinstance(left, BinaryExpression) else str(left)

            right_str = self._get_condition_string(right) \
                if isinstance(right, BinaryExpression) else str(right)

            return f"({left_str} {operator} {right_str})"

        if isinstance(left, IdentifierAstNode) and isinstance(right, NumericLiteralAstNode):
            return f"{left.name()} {operator} {right.value()}"

        raise ValueError("Invalid binary expression in WHERE clause")

    def _build_where_conditions(self, where_clause: WhereAstNode):
        where_conditions: list[str] = []

        for condition in where_clause.conditions():
            if isinstance(condition, BinaryExpression):
                where_conditions.append(self._get_condition_string(condition))
            else:
                raise ValueError(
                    "Only binary expressions are supported in WHERE clause conditions")

        return where_conditions

    def _execute_top_n_expression(self, select_clause: SelectClauseAstNode) -> DataFrame:
        top_n_expression = select_clause.from_clause().top_n_expression()
        n = self._calculate_top_n(top_n_expression)

        where_clause = select_clause.where_clause()
        where_conditions = self._build_where_conditions(
            where_clause) if where_clause else []

        order_by_clause = select_clause.order_by_clause()
        criteria = order_by_clause.criteria().name() if order_by_clause else "fitness"

        pattern = select_clause.pattern_matching_expression()
        pattern_str = pattern.to_string(0) if pattern else "None"

        logger.info("Executing TOP N expression", extra={
            "n": n,
            "where_conditions": where_conditions,
            "criteria": criteria,
            "pattern": pattern_str,
        })

        result = self._reggression.top(  # type: ignore
            n=n, filters=where_conditions, criteria=criteria)
        if not isinstance(result, DataFrame):
            raise ValueError(
                "Expected a DataFrame as a result of top N expression")

        logger.info(f"Executed TOP N expression with n={n}, result: {result}")

        return result

    def _execute_pareto_expression(self, select_clause: SelectClauseAstNode) -> DataFrame:
        result = self._reggression.pareto()  # type: ignore
        if not isinstance(result, DataFrame):
            raise ValueError(
                "Expected a DataFrame as a result of Pareto expression")

        logger.info(f"Executed Pareto expression, result: {result}")
        return result

    # TODO: Implement support for PATTERN MATCHING, and other SQL-like features.
    # TODO: Implement distribution analysis
    def execute(self) -> InferenceResultList:
        if not isinstance(self._root_node, SelectClauseAstNode):
            raise RootExpressionShouldBeSelectClauseError()

        for column in self._root_node.columns():
            if column.name().lower() not in self._QUERYABLE_LITERALS:
                raise ColumnIsNotSelectableError(column.name())

        from_kind = self._root_node.from_clause().source_kind()
        if from_kind == AstNodeKind.TOP_N_EXPRESSION:
            result = self._execute_top_n_expression(
                select_clause=self._root_node)

        elif from_kind == AstNodeKind.PARETO_EXPRESSION:
            result = self._execute_pareto_expression(self._root_node)
        else:
            raise ValueError(f"Unknown from kind: {from_kind}")

        subset = [column.name().lower()
                  for column in self._root_node.columns()]
        mask = result.columns.str.contains("|".join(subset), case=False)

        final_result = result.loc[:, mask]
        final_result.columns = final_result.columns.str.lower()

        results = [
            InferenceResult(**item) for  # type: ignore
            item in final_result.to_dict(orient="records")  # type: ignore
        ]

        return InferenceResultList(results=results)
