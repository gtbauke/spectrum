from iql.parser.parselets.errors.base import AbstractParseletError
from iql.parser.ast.base import BaseAstNode


class SelectClauseInvalidIdentifierError(AbstractParseletError):
    def __init__(self, node: BaseAstNode):
        super().__init__(node.span,
                         f"Expected identifier in SELECT list, but got {node.kind}")
