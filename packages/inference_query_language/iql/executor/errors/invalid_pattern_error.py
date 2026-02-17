from iql.executor.errors.base import QueryExecutionError


class InvalidPatternError(QueryExecutionError):
    def __init__(self):
        super().__init__("Invalid pattern")
