from iql.utils.span import Span

from .base import AbstractPlannerError


class ColumnIsNotQueryableError(AbstractPlannerError):
    def __init__(self, column_name: str, span: Span):
        super().__init__(span, f"Column '{column_name}' is not queryable.")
