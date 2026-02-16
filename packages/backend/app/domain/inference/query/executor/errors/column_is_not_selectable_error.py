from app.domain.inference.query.executor.errors.base import QueryExecutionError


class ColumnIsNotSelectableError(QueryExecutionError):
    def __init__(self, column_name: str):
        super().__init__(f"Column '{column_name}' is not selectable")
