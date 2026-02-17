from iql.executor.errors.base import QueryExecutionError


class InvalidBinaryConditionError(QueryExecutionError):
    def __init__(self):
        super().__init__("Invalid binary condition in WHERE clause")
