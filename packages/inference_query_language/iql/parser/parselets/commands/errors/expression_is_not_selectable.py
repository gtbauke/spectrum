from iql.parser.ast.base import AstNodeKind
from iql.parser.parselets.errors.base import AbstractParseletError
from iql.utils.span import Span


class ExpressionIsNotSelectableError(AbstractParseletError):
    def __init__(self, ast_node_kind: AstNodeKind, span: Span):
        super().__init__(
            span=span,
            message=f"Expression of kind {ast_node_kind} is not selectable in a SELECT clause")
