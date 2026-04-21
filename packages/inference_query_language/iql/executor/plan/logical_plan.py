from iql.executor.plan.environment import Environment
from iql.parser.ast.base import BaseAstNode


class LogicalPlan:
    def __init__(self, root: BaseAstNode, environment: Environment):
        self._root = root
        self._environment = environment
