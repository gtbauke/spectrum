from iql.executor.errors.base import QueryExecutionError
from iql.parser.ast.base import AstNodeKind


class InvalidFromSourceError(QueryExecutionError):
    def __init__(self, from_kind: AstNodeKind):
        super().__init__(
            f"'{from_kind}' is not a valid source for the FROM clause. Only TOP N and PARETO expressions are allowed.")
