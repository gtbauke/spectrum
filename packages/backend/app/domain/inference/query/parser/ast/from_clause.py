from typing import Union

from app.domain.inference.query.parser.ast.base import BaseAstNode, AstNodeKind
from app.domain.inference.query.parser.ast.top_n import TopNAstNode, ParetoAstNode
from app.domain.inference.query.span import Span


type FromClauseSource = Union[
    TopNAstNode,
    ParetoAstNode,
]


class FromAstNode(BaseAstNode):
    def __init__(self, source: FromClauseSource, span: Span):
        super().__init__(AstNodeKind.FROM_CLAUSE, span)
        self._source = source

    def to_string(self, indent: int) -> str:
        indent_str = " " * indent
        return f"{indent_str}FromAstNode:\n{self._source.to_string(indent + 2)}"

    def top_n_expression(self) -> TopNAstNode:
        if not isinstance(self._source, TopNAstNode):
            raise ValueError("From clause source is not a TopN expression")

        return self._source

    def pareto_expression(self) -> ParetoAstNode:
        if not isinstance(self._source, ParetoAstNode):
            raise ValueError("From clause source is not a Pareto expression")

        return self._source

    def source_kind(self) -> AstNodeKind:
        return self._source.kind
