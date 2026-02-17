from typing import Optional

from iql.parser.ast.base import AstNodeKind, BaseAstNode
from iql.parser.ast.identifier import IdentifierAstNode
from iql.parser.ast.from_clause import FromAstNode
from iql.parser.ast.order_by_clause import OrderByClauseAstNode
from iql.parser.ast.pattern_matching_expression import PatternMatchingExpression
from iql.parser.ast.where import WhereAstNode
from iql.utils.span import Span


class SelectClauseAstNode(BaseAstNode):
    def __init__(
        self,
        columns: list[IdentifierAstNode],
        span: Span,
        from_clause: FromAstNode,
        where_clause: Optional[WhereAstNode] = None,
        order_by_clause: Optional[OrderByClauseAstNode] = None,
        pattern_matching_expression: Optional[PatternMatchingExpression] = None
    ):
        super().__init__(AstNodeKind.SELECT_CLAUSE, span)
        self._columns = columns
        self._from_clause = from_clause
        self._where_clause = where_clause
        self._order_by_clause = order_by_clause
        self._pattern_matching_expression = pattern_matching_expression

    def columns(self) -> list[IdentifierAstNode]:
        return self._columns

    def from_clause(self) -> FromAstNode:
        return self._from_clause

    def where_clause(self) -> Optional[WhereAstNode]:
        return self._where_clause

    def order_by_clause(self) -> Optional[OrderByClauseAstNode]:
        return self._order_by_clause

    def pattern_matching_expression(self) -> Optional[PatternMatchingExpression]:
        return self._pattern_matching_expression

    def to_string(self, indent: int) -> str:
        indent_str = " " * indent
        columns_str = ", ".join(column.to_string(0)
                                for column in self._columns)
        from_clause_str = self._from_clause.to_string(
            indent + 2) if self._from_clause else ""
        where_clause_str = self._where_clause.to_string(
            indent + 2) if self._where_clause else ""
        order_by_clause_str = self._order_by_clause.to_string(
            indent + 2) if self._order_by_clause else ""
        pattern_matching_expression_str = self._pattern_matching_expression.to_string(
            indent + 2) if self._pattern_matching_expression else ""

        return f"{indent_str}SELECT {columns_str}\n{from_clause_str}{where_clause_str}{order_by_clause_str}{pattern_matching_expression_str}"
