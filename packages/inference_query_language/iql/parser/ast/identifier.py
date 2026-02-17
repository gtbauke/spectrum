from iql.parser.ast.base import AstNodeKind, BaseAstNode
from iql.utils.span import Span


class IdentifierAstNode(BaseAstNode):
    def __init__(self, name: str, span: Span):
        super().__init__(AstNodeKind.IDENTIFIER, span)
        self._name = name

    def to_string(self, indent: int) -> str:
        return f"{' ' * indent}Identifier: {self._name}"

    def name(self) -> str:
        return self._name
