from iql.analyzer.errors import AbstractAnalyzerError
from iql.utils.span import Span


class ColumnNotSelectableError(AbstractAnalyzerError):
    """Raised when a column identifier is not in the set of queryable columns."""

    def __init__(self, column_name: str, span: Span):
        self.column_name = column_name
        super().__init__(span, f"Column '{column_name}' is not selectable.")


class ModelNotFoundError(AbstractAnalyzerError):
    """Raised when the FROM model cannot be resolved."""

    def __init__(self, model_name: str, span: Span):
        self.model_name = model_name
        super().__init__(span, f"Model '{model_name}' was not found.")


class UnknownFunctionError(AbstractAnalyzerError):
    """Raised when a function call references a name not in the registry."""

    def __init__(self, function_name: str, span: Span):
        self.function_name = function_name
        super().__init__(span, f"Unknown function '{function_name}'.")


class RootNodeNotSelectError(AbstractAnalyzerError):
    """Raised when the AST root is not a SELECT command."""

    def __init__(self, span: Span):
        super().__init__(span, "Root expression must be a SELECT clause.")


class InvalidWhereIdentifierError(AbstractAnalyzerError):
    """Raised when a WHERE clause references an unsupported column."""

    def __init__(self, identifier_name: str, span: Span):
        self.identifier_name = identifier_name
        super().__init__(
            span,
            f"Identifier '{identifier_name}' cannot be used in WHERE conditions.",
        )
