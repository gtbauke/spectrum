from app.domain.inference.query.parser.ast.base import BaseAstNode, AstNodeKind
from app.domain.inference.query.parser.ast.top_n import TopNAstNode
from app.domain.inference.query.span import Span


class FromAstNode(BaseAstNode):
    def __init__(self, source: TopNAstNode, span: Span):
        super().__init__(AstNodeKind.FROM_CLAUSE, span)
        self._source = source

    def to_string(self, indent: int) -> str:
        indent_str = " " * indent
        return f"{indent_str}FromAstNode:\n{self._source.to_string(indent + 2)}"
