from iql.parser.ast.base import BaseAstNode, AstNodeKind
from iql.parser.ast.identifier import IdentifierAstNode


class AliasClauseAstNode(BaseAstNode):
    def __init__(self, alias: IdentifierAstNode, span):
        super().__init__(AstNodeKind.ALIAS_CLAUSE, span)
        self._alias = alias

    def alias(self) -> IdentifierAstNode:
        return self._alias
