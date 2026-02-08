from app.domain.inference.query.parser.ast.base import AstNodeKind, BaseAstNode
from app.domain.inference.query.span import Span


class IdentifierAstNode(BaseAstNode):
    def __init__(self, name: str, span: Span):
        super().__init__(AstNodeKind.IDENTIFIER, span)
        self._name = name
