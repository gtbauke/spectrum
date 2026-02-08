from typing import Optional
from app.domain.inference.query.parser.ast.base import AstNodeKind, BaseAstNode
from app.domain.inference.query.parser.ast.identifier import IdentifierAstNode
from app.domain.inference.query.parser.ast.from_clause import FromAstNode
from app.domain.inference.query.span import Span


class SelectClauseAstNode(BaseAstNode):
    def __init__(
        self,
        columns: list[IdentifierAstNode],
        from_clause: Optional[FromAstNode],
        span: Span
    ):
        super().__init__(AstNodeKind.SELECT_CLAUSE, span)
        self._columns = columns
        self._from_clause = from_clause
