from iql.parser.ast.base import BaseAstNode, AstNodeKind
from iql.utils.span import Span


class StringLiteralAstNode(BaseAstNode):
    def __init__(self, value: str, span: Span):
        super().__init__(AstNodeKind.STRING_LITERAL, span)
        self._value = value

    @property
    def value(self) -> str:
        return self._value

    def to_string(self, indent: int) -> str:
        return f"StringLiteral(value='{self._value}')"
