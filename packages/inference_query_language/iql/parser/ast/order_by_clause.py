from iql.parser.ast.base import BaseAstNode, AstNodeKind
from iql.parser.ast.identifier import IdentifierAstNode
from iql.utils.span import Span


class OrderByClauseAstNode(BaseAstNode):
    def __init__(self, criteria: IdentifierAstNode, span: Span):
        super().__init__(AstNodeKind.ORDER_CLAUSE, span)
        self._criteria = criteria

    def to_string(self, indent: int) -> str:
        return " " * indent + f"OrderByClause(criteria={self._criteria})"

    def criteria(self) -> IdentifierAstNode:
        return self._criteria
