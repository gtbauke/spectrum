from app.domain.inference.query.parser.ast.base import BaseAstNode, AstNodeKind
from app.domain.inference.query.span import Span


class NumericLiteralAstNode(BaseAstNode):
    pass


class IntegerLiteralAstNode(NumericLiteralAstNode):
    def __init__(self, value: int, span: Span):
        self._value = value
        super().__init__(AstNodeKind.INTEGER_LITERAL, span)


class FloatLiteralAstNode(NumericLiteralAstNode):
    def __init__(self, value: float, span: Span):
        self._value = value
        super().__init__(AstNodeKind.FLOAT_LITERAL, span)
