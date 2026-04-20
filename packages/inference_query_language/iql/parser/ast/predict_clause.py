from iql.parser.ast.base import AstNodeKind, BaseAstNode
from iql.parser.ast.identifier import IdentifierAstNode
from iql.parser.ast.number import NumericLiteralAstNode
from iql.utils.span import Span


class PredictMapping:
    def __init__(self, variable: IdentifierAstNode, value: NumericLiteralAstNode):
        self.variable = variable
        self.value = value


class PredictClauseAstNode(BaseAstNode):
    def __init__(self, mappings: list[PredictMapping], span: Span):
        super().__init__(AstNodeKind.PREDICT_CLAUSE, span)
        self._mappings = mappings

    @property
    def mappings(self) -> list[PredictMapping]:
        return self._mappings

    def to_string(self, indent: int) -> str:
        mappings_str = ", ".join(
            f"{m.variable.name}={m.value.value}" for m in self._mappings)
        return f"PREDICT({mappings_str})"
