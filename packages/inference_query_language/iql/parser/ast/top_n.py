from typing import Optional

from iql.utils.span import Span
from iql.parser.ast.base import BaseAstNode, AstNodeKind


class TopNAstNode(BaseAstNode):
    def __init__(self, top_n: Optional[BaseAstNode], span: Span):
        super().__init__(AstNodeKind.TOP_N_EXPRESSION, span)
        self._top_n = top_n

    def top_n(self) -> Optional[BaseAstNode]:
        return self._top_n

    def to_string(self, indent: int) -> str:
        return f"{' ' * indent}TOP_N({self._top_n.to_string(0) if self._top_n else 'None'})"


class ParetoAstNode(BaseAstNode):
    def __init__(self, span: Span):
        super().__init__(AstNodeKind.PARETO_EXPRESSION, span)

    def to_string(self, indent: int) -> str:
        return f"{' ' * indent}PARETO()"
