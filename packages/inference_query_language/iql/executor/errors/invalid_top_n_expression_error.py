from iql.executor.errors.base import QueryExecutionError


class InvalidTopNExpressionError(QueryExecutionError):
    def __init__(self, expression_kind: type):
        super().__init__(
            f"'{expression_kind}' is not a valid expression for TOP N. Only integer literals are allowed.")
