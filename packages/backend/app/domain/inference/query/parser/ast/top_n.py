from typing import Optional

from app.domain.inference.query.span import Span
from app.domain.inference.query.parser.ast.base import BaseAstNode, AstNodeKind


class TopNAstNode(BaseAstNode):
    def __init__(self, top_n: Optional[BaseAstNode], span: Span):
        super().__init__(AstNodeKind.TOP_N_EXPRESSION, span)
        self._top_n = top_n
