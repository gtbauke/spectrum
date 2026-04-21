from iql.parser.ast.base import BaseAstNode, AstNodeKind
from iql.parser.ast.string import StringLiteralAstNode
from iql.utils.span import Span


class PatternMatchingExpression(BaseAstNode):
    def __init__(self, pattern: StringLiteralAstNode, span: Span):
        super().__init__(AstNodeKind.PATTERN_MATCHING_EXPRESSION, span)
        self._pattern = pattern

    def to_string(self, indent: int) -> str:
        return f"{' ' * indent}IS LIKE\n{self._pattern.to_string(indent + 2)}"

    @property
    def pattern(self) -> StringLiteralAstNode:
        return self._pattern
