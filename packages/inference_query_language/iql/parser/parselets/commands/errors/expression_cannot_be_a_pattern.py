from iql.parser.ast.base import AstNodeKind
from iql.parser.parselets.errors.base import AbstractParseletError
from iql.utils.span import Span


class ExpressionCannotBeAPatternError(AbstractParseletError):
    def __init__(self, expression_kind: AstNodeKind, span: Span):
        super().__init__(
            span,
            f"Expression of kind {expression_kind} cannot be used as a pattern",
        )
