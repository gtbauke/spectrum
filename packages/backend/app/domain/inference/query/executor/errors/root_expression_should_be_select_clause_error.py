from app.domain.inference.query.executor.errors.base import QueryExecutionError


class RootExpressionShouldBeSelectClauseError(QueryExecutionError):
    def __init__(self) -> None:
        super().__init__("The root expression of the query should be a SELECT clause.")
