from app.domain.inference.query.parser.ast.base import BaseAstNode, AstNodeKind
from app.domain.inference.query.span import Span


class WhereAstNode(BaseAstNode):
    def __init__(self, conditions: list[BaseAstNode], span: Span):
        self._conditions = conditions
        super().__init__(AstNodeKind.WHERE_CLAUSE, span)

    def to_string(self, indent: int) -> str:
        indent_str = " " * indent
        conditions_str = "\n".join(
            condition.to_string(indent + 2) for condition in self._conditions
        )

        return f"{indent_str}WHERE\n{conditions_str}"
