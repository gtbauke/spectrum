from iql.executor.plan.environment import EntryType, Environment
from iql.executor.plan.errors.base import AbstractPlannerError
from iql.executor.plan.errors.column_is_not_queryable import ColumnIsNotQueryableError
from iql.executor.plan.errors.model_is_not_available import ModelIsNotAvailableError
from iql.executor.plan.logical_plan import LogicalPlan
from iql.executor.query_executor import SelectCommandAstNode
from iql.parser.ast.base import BaseAstNode
from iql.utils.planner_constants import PREDICT_FUNCTION_NAME, QUERYABLE_LITERALS


class Model:
    def __init__(self, *, id: str, name: str):
        self.id = id
        self.name = name


class Planner:
    def __init__(self, root: BaseAstNode, available_models: list[Model]):
        self._environment = Environment()
        self._root = root
        self._errors: list[AbstractPlannerError] = []
        self._available_models = available_models

    def _initialize_plan_environment(self):
        self._environment.set_variable(
            entry_type=EntryType.FUNCTION,
            name=PREDICT_FUNCTION_NAME,
            value=lambda *args, **kwargs: None
        )

    def create_plan(self) -> LogicalPlan:
        self._initialize_plan_environment()

        if isinstance(self._root, SelectCommandAstNode):
            for identifier in self._root.columns():
                if identifier.name() in QUERYABLE_LITERALS:
                    self._environment.set_variable(
                        entry_type=EntryType.VARIABLE,
                        name=identifier.name(),
                        value=None
                    )

                if identifier.name() not in QUERYABLE_LITERALS:
                    self._errors.append(
                        ColumnIsNotQueryableError(
                            span=identifier.span,
                            column_name=identifier.name(),
                        )
                    )

            selected_model = None
            for model in self._available_models:
                if model.name == self._root.from_model().name():
                    selected_model = model
                    break

                if model.id == self._root.from_model().name():
                    selected_model = model
                    break

            if not selected_model:
                self._errors.append(
                    ModelIsNotAvailableError(
                        span=self._root.from_model().span,
                        model_name=self._root.from_model().name(),
                        model_id=self._root.from_model().name(),
                    )
                )

        return LogicalPlan(root=self._root, environment=self._environment)
