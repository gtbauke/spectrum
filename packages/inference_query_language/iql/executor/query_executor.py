import logging

from pandas import DataFrame
from reggression import Reggression  # type: ignore

from iql.executor.errors.invalid_binary_condition_error import InvalidBinaryConditionError
from iql.executor.errors.invalid_condition_identifier_error import InvalidConditionIdentifierError
from iql.executor.errors.invalid_from_source_error import InvalidFromSourceError
from iql.executor.errors.invalid_pattern_error import InvalidPatternError
from iql.executor.errors.invalid_pattern_matching_operator_error import InvalidPatternMatchingOperatorError
from iql.executor.errors.invalid_top_n_expression_error import InvalidTopNExpressionError
from iql.executor.errors.result_should_be_dataframe_error import ResultShouldBeDataFrameError
from iql.executor.errors.column_is_not_selectable_error import ColumnIsNotSelectableError

from iql.parser.ast.where import WhereAstNode
from iql.parser.base import BaseAstNode
from iql.parser.ast.base import AstNodeKind
from iql.parser.ast.select import IdentifierAstNode, PatternMatchingExpression, SelectClauseAstNode
from iql.executor.errors.root_expression_should_be_select_clause_error import (
    RootExpressionShouldBeSelectClauseError,
)
from iql.parser.ast.top_n import TopNAstNode
from iql.parser.ast.number import IntegerLiteralAstNode, NumericLiteralAstNode
from iql.parser.ast.binary_expression import BinaryExpression
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

    _ACCEPTED_WHERE_LITERALS = (
        "size",
        "parameters",
        "cost",
    )

    def __init__(self, root_node: BaseAstNode, reggressions: dict[str, Reggression]):
        self._root_node = root_node
        self._reggressions = reggressions
        self._active_reggression: Optional[Reggression] = None

    def _calculate_node_value(self, node: BaseAstNode):
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

        if not isinstance(n_value, int):
            raise InvalidTopNExpressionError(type(value))

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

            return f"{left_str} {operator} {right_str}"

        if isinstance(left, IdentifierAstNode) and isinstance(right, NumericLiteralAstNode):
            if left.name() not in self._ACCEPTED_WHERE_LITERALS:
                raise InvalidConditionIdentifierError(left.name())

            return f"{left.name()} {operator} {right.value()}"

        raise InvalidBinaryConditionError()

    def _build_where_conditions(self, where_clause: WhereAstNode):
        where_conditions: list[str] = []

        for condition in where_clause.conditions():
            if isinstance(condition, BinaryExpression):
                condition = self._get_condition_string(condition)

                if "AND" in condition:
                    broken_conditions = condition.split("AND")
                    where_conditions.extend([c.strip()
                                            for c in broken_conditions])
            else:
                raise InvalidBinaryConditionError()

        return where_conditions

    def _build_pattern_string(self, pattern: BaseAstNode) -> str:
        if isinstance(pattern, IdentifierAstNode):
            return pattern.name()

        if isinstance(pattern, BinaryExpression):
            operator = pattern.operator()

            if not operator.is_arithmetic_operator():
                raise InvalidPatternMatchingOperatorError(operator)

            left = self._build_pattern_string(pattern.left())
            right = self._build_pattern_string(pattern.right())

            return f"{left}{operator}{right}"

        raise InvalidPatternError()

    def _build_pattern_matching(self, pattern_matching_clause: PatternMatchingExpression) -> str:
        pattern = pattern_matching_clause.pattern
        return self._build_pattern_string(pattern)

    def _execute_top_n_expression(self, select_clause: SelectClauseAstNode, modifier: TopNAstNode) -> DataFrame:
        n = self._calculate_top_n(modifier)

        where_clause = select_clause.where_clause()
        where_conditions = self._build_where_conditions(
            where_clause) if where_clause else []

        pattern = select_clause.pattern_matching_expression()
        pattern_str = self._build_pattern_matching(pattern) if pattern else ""

        order_by_clause = select_clause.order_by_clause()
        criteria = order_by_clause.criteria().name() if order_by_clause else "fitness"

        if self._active_reggression is None:
            raise ValueError("No active regression object set")

        result = self._active_reggression.top(  # type: ignore
            n=n,
            filters=where_conditions,
            criteria=criteria,
            pattern=pattern_str
        )

        if not isinstance(result, DataFrame):
            raise ResultShouldBeDataFrameError()

        return result

    def _execute_pareto_expression(self) -> DataFrame:
        if self._active_reggression is None:
            raise ValueError("No active regression object set")

        result = self._active_reggression.pareto()  # type: ignore

        if not isinstance(result, DataFrame):
            raise ResultShouldBeDataFrameError()

        return result

    # TODO: Implement support for other SQL-like features.
    # TODO: Implement distribution analysis
    def execute(self) -> InferenceResultList:
        if not isinstance(self._root_node, SelectClauseAstNode):
            raise RootExpressionShouldBeSelectClauseError()

        for column in self._root_node.columns():
            if column.name().lower() not in self._QUERYABLE_LITERALS:
                raise ColumnIsNotSelectableError(column.name())

        model_identifier = self._root_node.from_clause().identifier().name()
        if model_identifier not in self._reggressions:
            raise InvalidFromSourceError(model_identifier)
        
        self._active_reggression = self._reggressions[model_identifier]

        modifier = self._root_node.modifier()

        if isinstance(modifier, TopNAstNode):
            result = self._execute_top_n_expression(
                select_clause=self._root_node, modifier=modifier)
        elif isinstance(modifier, ParetoAstNode):
            result = self._execute_pareto_expression()
        elif modifier is None:
            # Default to TOP 10 if no modifier is provided
            default_top_n = TopNAstNode(None, self._root_node.span)
            result = self._execute_top_n_expression(
                select_clause=self._root_node, modifier=default_top_n)
        else:
            raise InvalidFromSourceError(type(modifier))

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
