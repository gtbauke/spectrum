import logging
from pandas import DataFrame
from reggression import Reggression  # type: ignore

from iql.compiler import LogicalPlan
from iql.executor.errors.base import QueryExecutionError
from iql.executor.errors.result_should_be_dataframe_error import ResultShouldBeDataFrameError

from iql.executor.plan.nodes import (
    ApplyNode,
    FilterNode,
    LogicalPlanNode,
    ProjectNode,
    ScanNode,
    SearchMode,
    SearchNode,
)
from iql.utils.result import InferenceResult, InferenceResultList

logger = logging.getLogger(__name__)


class ExecutorContext:
    def __init__(self, reggressions: dict[str, Reggression]):
        self.reggressions = reggressions
        self.active_reggression: Reggression | None = None
        self.filters: list[str] = []
        self.dataframe: DataFrame | None = None
        self.project_columns: list[str] = []


class QueryExecutor:
    """Interprets a LogicalPlan and executes it against Reggression objects."""

    def __init__(self, plan: LogicalPlan, reggressions: dict[str, Reggression]):
        self._plan = plan
        self._context = ExecutorContext(reggressions)

    def execute(self) -> InferenceResultList:
        self._process_node(self._plan.root)

        df = self._context.dataframe
        if df is None:
            raise QueryExecutionError("Execution failed to produce a result.")

        return self._format_results(df)

    def _process_node(self, node: LogicalPlanNode | None) -> None:
        if node is None:
            return

        # Bottom-up evaluation
        self._process_node(node.child)

        if isinstance(node, ScanNode):
            self._execute_scan(node)
        elif isinstance(node, FilterNode):
            self._execute_filter(node)
        elif isinstance(node, SearchNode):
            self._execute_search(node)
        elif isinstance(node, ApplyNode):
            self._execute_apply(node)
        elif isinstance(node, ProjectNode):
            self._context.project_columns = node.columns
        else:
            raise QueryExecutionError(f"Unsupported plan node: {type(node)}")

    def _execute_scan(self, node: ScanNode) -> None:
        if node.model_name not in self._context.reggressions:
            raise QueryExecutionError(
                f"Model '{node.model_name}' not found in registry.")
        self._context.active_reggression = self._context.reggressions[node.model_name]

    def _execute_filter(self, node: FilterNode) -> None:
        # Accumulate filters to be used by the SearchNode
        self._context.filters.extend(node.conditions)

    def _execute_search(self, node: SearchNode) -> None:
        regg = self._context.active_reggression
        if not regg:
            raise QueryExecutionError(
                "SearchNode executed before ScanNode (no active regression).")

        filters = self._context.filters
        pattern = node.pattern if node.pattern else ""

        if node.mode == SearchMode.TOP_N:
            result = regg.top(n=node.n or 1, filters=filters, pattern=pattern)
        elif node.mode == SearchMode.PARETO:
            result = regg.pareto()
        elif node.mode == SearchMode.DISTRIBUTION:
            result = regg.distribution(
                filters=filters,
                limitedAt=node.limit or 1000,
                atLeast=node.at_least or 10,
                fromTop=node.n or 5000,
            )
        else:
            raise QueryExecutionError(f"Unknown search mode: {node.mode}")

        if not isinstance(result, DataFrame):
            raise ResultShouldBeDataFrameError()

        self._context.dataframe = result

    def _execute_apply(self, node: ApplyNode) -> None:
        df = self._context.dataframe
        if df is None:
            raise QueryExecutionError(
                "ApplyNode executed before returning a DataFrame.")

        if node.function_name.upper() == "PREDICT":
            from core.features.profiles.blocks.inference.prediction_service import PredictionEvaluationService
            service = PredictionEvaluationService()

            predictions = []
            for _, row in df.iterrows():
                expr = row.get("expression", row.get(
                    "Pattern", row.get("Numpy", "")))
                params = row.get("parameters", row.get("Parameters", "[]"))
                pred = service.evaluate_expression(
                    expr, node.arguments, params)
                predictions.append(pred.tolist())

            df["prediction"] = predictions
            self._context.dataframe = df
        else:
            raise QueryExecutionError(
                f"Unsupported built-in function: {node.function_name}")

    def _format_results(self, df: DataFrame) -> InferenceResultList:
        result = df.copy()
        subset = self._context.project_columns

        # Ensure consistent column naming internally mapping to IQL expectations
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
            # Ensure egraph_id is a string as expected by InferenceResult DTO
            result["egraph_id"] = result["egraph_id"].astype(str)
            subset = ["egraph_id" if c == "id" else c for c in subset]
            if "egraph_id" not in subset:
                subset.append("egraph_id")

        if "Fitness" in result.columns:
            result = result.rename(columns={"Fitness": "fitness"})
            subset = ["fitness" if c == "fitness" else c for c in subset]

        if "Numpy" in result.columns:
            result = result.rename(columns={"Numpy": "numpy"})
            subset = ["numpy" if c == "numpy" else c for c in subset]

        # Project columns
        mask = result.columns.str.contains("|".join(subset), case=False)
        final_result = result.loc[:, mask]
        final_result.columns = final_result.columns.str.lower()

        logger.info(f"Final result columns: {final_result.columns.tolist()}")

        results = [
            InferenceResult(**item)  # type: ignore
            for item in final_result.to_dict(orient="records")  # type: ignore
        ]

        return InferenceResultList(results=results)
