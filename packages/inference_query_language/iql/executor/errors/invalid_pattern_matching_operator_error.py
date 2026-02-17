from iql.executor.errors.base import QueryExecutionError
from iql.parser.ast.binary_expression import BinaryOperator


class InvalidPatternMatchingOperatorError(QueryExecutionError):
    def __init__(self, operator: BinaryOperator):
        super().__init__(
            f"Invalid pattern matching operator '{operator}'. Only arithmetic operators are allowed in pattern matching expressions.")
