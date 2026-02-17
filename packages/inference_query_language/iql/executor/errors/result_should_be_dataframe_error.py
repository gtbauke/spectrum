from iql.executor.errors.base import QueryExecutionError


class ResultShouldBeDataFrameError(QueryExecutionError):
    def __init__(self):
        super().__init__("Expected a DataFrame as a result, but got something else")
