from typing import Optional
from app.domain.inference.query.parser.ast.base import AstNodeKind, BaseAstNode
from app.domain.inference.query.parser.ast.identifier import IdentifierAstNode
from app.domain.inference.query.parser.ast.from_clause import FromAstNode
from app.domain.inference.query.parser.ast.where import WhereAstNode
from app.domain.inference.query.span import Span


class SelectClauseAstNode(BaseAstNode):
    def __init__(
        self,
        columns: list[IdentifierAstNode],
        span: Span,
        from_clause: FromAstNode,
        where_clause: Optional[WhereAstNode] = None,
    ):
        super().__init__(AstNodeKind.SELECT_CLAUSE, span)
        self._columns = columns
        self._from_clause = from_clause
        self._where_clause = where_clause

    def columns(self) -> list[IdentifierAstNode]:
        return self._columns

    def from_clause(self) -> FromAstNode:
        return self._from_clause

    def where_clause(self) -> Optional[WhereAstNode]:
        return self._where_clause

    def to_string(self, indent: int) -> str:
        indent_str = " " * indent
        columns_str = ", ".join(column.to_string(0)
                                for column in self._columns)
        from_clause_str = self._from_clause.to_string(
            indent + 2) if self._from_clause else ""
        where_clause_str = self._where_clause.to_string(
            indent + 2) if self._where_clause else ""

        return f"{indent_str}SELECT {columns_str}\n{from_clause_str}{where_clause_str}"
