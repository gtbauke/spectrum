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

from iql.parser.ast.commands.select_command import SelectCommandAstNode
from iql.parser.ast.function_call import FunctionCallAstNode
from iql.parser.ast.identifier import IdentifierAstNode
from iql.parser.ast.pattern_matching_expression import PatternMatchingExpression
from iql.parser.ast.where import WhereAstNode
from iql.parser.base import BaseAstNode
from iql.parser.ast.base import AstNodeKind
from iql.executor.errors.root_expression_should_be_select_clause_error import (
    RootExpressionShouldBeSelectClauseError,
)
from iql.parser.ast.top_n import ParetoAstNode, TopNAstNode
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
        "pattern",
        "frequency",
        "prediction",
    )

    _ACCEPTED_WHERE_LITERALS = (
        "id",
        "size",
        "parameters",
        "cost",
    )

    def __init__(self, root_node: BaseAstNode, reggressions: dict[str, Reggression]):
        self._root_node = root_node
        self._reggressions = reggressions
        self._active_reggression: Reggression | None = None

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

    def _execute_top_n_expression(self, select_clause: SelectCommandAstNode, modifier: TopNAstNode) -> DataFrame:
        n = self._calculate_top_n(modifier)

        where_clause = select_clause.where()
        where_conditions = self._build_where_conditions(
            where_clause) if where_clause else []

        pattern = select_clause.pattern_matching_expression()
        pattern_str = self._build_pattern_matching(pattern) if pattern else ""

        order_by_clause = select_clause.order_by()
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

    def _execute_distribution_expression(self, select_clause: SelectCommandAstNode) -> DataFrame:
        modifier = select_clause.modifier()
        from_top = self._calculate_top_n(
            modifier) if isinstance(modifier, TopNAstNode) else 5000

        where_clause = select_clause.where()
        filters = self._build_where_conditions(
            where_clause) if where_clause else []

        at_least_node = select_clause.at_least()
        if not isinstance(at_least_node, IntegerLiteralAstNode):
            raise ValueError(
                "AT LEAST modifier must be an integer literal")

        at_least = at_least_node.value() if at_least_node else 10

        limit_node = select_clause.limit()
        limited_at = limit_node.value() if limit_node else 1000

        order_by_clause = select_clause.order_by()
        by_fitness = True
        dsc = True

        if order_by_clause:
            criteria = order_by_clause.criteria().name().lower()
            by_fitness = criteria == "fitness"
            # In current IQL, ORDER BY is always interpreted as DESC if it's the default,
            # or we might need explicit DESC/ASC tokens which aren't fully implemented as flags yet.
            # For distribution, we'll assume the intention is DESC (top models).

        if self._active_reggression is None:
            raise ValueError("No active regression object set")

        result = self._active_reggression.distribution(  # type: ignore
            filters=filters,
            limitedAt=limited_at,
            dsc=dsc,
            byFitness=by_fitness,
            atLeast=at_least,
            fromTop=from_top
        )

        if not isinstance(result, DataFrame):
            raise ResultShouldBeDataFrameError()

        return result

    # TODO: Implement support for other SQL-like features.
    def execute(self) -> InferenceResultList:
        if not isinstance(self._root_node, SelectCommandAstNode):
            raise RootExpressionShouldBeSelectClauseError()

        for column in self._root_node.columns():
            col_name = "prediction" if isinstance(
                column, FunctionCallAstNode) else column.name().lower()
            if col_name not in self._QUERYABLE_LITERALS:
                raise ColumnIsNotSelectableError(col_name)

        model_identifier = self._root_node.from_model()

        logger.info(
            f"[QueryExecutor] Executing query for model: {model_identifier.name()}")
        logger.info(
            f"[QueryExecutor] Available reggressions: {list(self._reggressions.keys())}")

        if model_identifier.name() not in self._reggressions:
            raise InvalidFromSourceError(model_identifier.kind)

        self._active_reggression = self._reggressions[model_identifier.name()]

        modifier = self._root_node.modifier()

        if self._root_node.is_distribution():
            result = self._execute_distribution_expression(self._root_node)
        elif isinstance(modifier, TopNAstNode):
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
            raise InvalidFromSourceError(modifier.kind)

        predict_clauses = [col for col in self._root_node.columns(
        ) if isinstance(col, FunctionCallAstNode)]

        subset = ["prediction" if isinstance(column, FunctionCallAstNode) else column.name().lower()
                  for column in self._root_node.columns()]

        logger.info(f"Raw result columns: {result.columns.tolist()}")
        logger.info(f"Raw result sample:\n{result.head()}")

        # Map 'pattern' column to 'expression' in the final result for consistency
        if "Pattern" in result.columns:
            result = result.rename(columns={"Pattern": "expression"})
            subset = ["expression" if c == "pattern" else c for c in subset]

        if "Count" in result.columns:
            result = result.rename(columns={"Count": "frequency"})
            subset = ["frequency" if c == "count" else c for c in subset]

        if "AvgFit" in result.columns:
            result = result.rename(columns={"AvgFit": "fitness"})
            subset = ["fitness" if c == "avgfit" else c for c in subset]

        if "Id" in result.columns:
            result = result.rename(columns={"Id": "egraph_id"})
            subset = ["egraph_id" if c == "id" else c for c in subset]
            # Force inclusion of egraph_id for predictability across backend lookups
            if "egraph_id" not in subset:
                subset.append("egraph_id")

        if predict_clauses:
            from core.features.profiles.blocks.inference.prediction_service import PredictionEvaluationService
            service = PredictionEvaluationService()

            # Use the first PREDICT clause
            predict_clause = predict_clauses[0]
            variables = {m.variable.name(): [m.value.value()]
                         for m in predict_clause.arguments}

            predictions = []
            for _, row in result.iterrows():
                expr = row.get("expression", row.get(
                    "Pattern", row.get("Numpy", "")))
                params = row.get("parameters", row.get("Parameters", "[]"))
                pred = service.evaluate_expression(expr, variables, params)
                predictions.append(pred.tolist())

            result["prediction"] = predictions

        mask = result.columns.str.contains("|".join(subset), case=False)

        final_result = result.loc[:, mask]
        final_result.columns = final_result.columns.str.lower()

        logger.info(
            f"Final result columns after filtering and renaming: {final_result.columns.tolist()}")
        logger.info(f"Final result sample:\n{final_result.head()}")

        results = [
            InferenceResult(**item) for  # type: ignore
            item in final_result.to_dict(orient="records")  # type: ignore
        ]

        return InferenceResultList(results=results)
