from iql.parser.ast.base import AstNodeKind
from iql.parser.parselets.errors.base import AbstractParseletError
from iql.utils.span import Span


class ExpressionIsNotNumericError(AbstractParseletError):
    def __init__(self, expression_kind: AstNodeKind, span: Span):
        message = f"Expected a numeric expression, but got {expression_kind}"
        super().__init__(span, message)
