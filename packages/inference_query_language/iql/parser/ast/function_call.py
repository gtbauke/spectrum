from iql.parser.ast.base import AstNodeKind, BaseAstNode
from iql.parser.ast.identifier import IdentifierAstNode
from iql.parser.ast.number import NumericLiteralAstNode
from iql.utils.span import Span


class FunctionArgument:
    def __init__(self, variable: IdentifierAstNode, value: NumericLiteralAstNode):
        self.variable = variable
        self.value = value


class FunctionCallAstNode(BaseAstNode):
    def __init__(self, function_name: str, arguments: list[FunctionArgument], span: Span):
        super().__init__(AstNodeKind.FUNCTION_CALL, span)
        self._function_name = function_name
        self._arguments = arguments

    @property
    def function_name(self) -> str:
        return self._function_name

    def name(self) -> str:
        return self._function_name.lower()

    @property
    def arguments(self) -> list[FunctionArgument]:
        return self._arguments

    def to_string(self, indent: int) -> str:
        args_str = ", ".join(
            f"{a.variable.name}={a.value.value}" for a in self._arguments)
        return f"{self._function_name}({args_str})"
