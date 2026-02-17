from iql.executor.errors.base import QueryExecutionError


class InvalidConditionIdentifierError(QueryExecutionError):
    def __init__(self, identifier: str):
        super().__init__(
            f"Invalid condition identifier: '{identifier}' is not a valid condition identifier.")
