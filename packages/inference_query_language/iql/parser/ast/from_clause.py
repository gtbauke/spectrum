from typing import Union

from iql.parser.ast.base import BaseAstNode, AstNodeKind
from iql.parser.ast.identifier import IdentifierAstNode
from iql.utils.span import Span


class FromAstNode(BaseAstNode):
    def __init__(
        self,
        identifier: IdentifierAstNode,
        span: Span
    ):
        super().__init__(AstNodeKind.FROM_CLAUSE, span)
        self._identifier = identifier

    def to_string(self, indent: int) -> str:
        indent_str = " " * indent
        return f"{indent_str}FromAstNode:\n{self._identifier.to_string(indent + 2)}"

    def identifier(self) -> IdentifierAstNode:
        return self._identifier
