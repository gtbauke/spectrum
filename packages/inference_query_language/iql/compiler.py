from __future__ import annotations

import logging
import traceback

from iql.analyzer.analyzer import AnalysisContext, SemanticAnalyzer
from iql.errors.collector import IqlErrorCollector
from iql.executor.plan.nodes import LogicalPlan
from iql.executor.plan.planner import Planner
from iql.parser.parser import InferenceQueryParser
from iql.registry.function import create_default_registry
from iql.tokenizer.tokenizer import QueryTokenizer
from iql.utils.span import Span
from iql.errors.base import AbstractInferenceQueryLanguageError

logger = logging.getLogger(__name__)


class CompilerResult:
    """The result of an IQL compilation pass."""

    def __init__(self, plan: LogicalPlan | None, errors: IqlErrorCollector, resolved_model_identifier: str | None = None):
        self.plan = plan
        self.errors = errors
        self.resolved_model_identifier = resolved_model_identifier

    @property
    def is_success(self) -> bool:
        return self.plan is not None and not self.errors.has_errors()


class IqlCompiler:
    """Orchestrates the entire IQL pipeline from string to LogicalPlan.

    Pipeline phases:
    1. Tokenize (String -> Tokens)
    2. Parse (Tokens -> AST)
    3. Analyze (AST -> Semantic bindings & type checks)
    4. Plan (AST + Context -> LogicalPlan)
    """

    def __init__(self) -> None:
        self._registry = create_default_registry()

    def compile(self, query: str, available_models: list[str]) -> CompilerResult:
        errors = IqlErrorCollector()

        try:
            tokenizer = QueryTokenizer(query)
            tokens = tokenizer.tokenize()

            parser = InferenceQueryParser(tokens)
            ast = parser.parse_expression()

            context = AnalysisContext(
                available_model_names=available_models,
                function_registry=self._registry,
            )

            analyzer = SemanticAnalyzer(context)
            analysis_result = analyzer.analyze(ast)

            for err in analysis_result.errors.errors:
                errors.add(err)

            if errors.has_errors():
                return CompilerResult(plan=None, errors=errors)

            planner = Planner(
                root=ast, analysis=analysis_result, errors=errors)
            logical_plan = planner.create_plan()

            return CompilerResult(plan=logical_plan, errors=errors, resolved_model_identifier=analysis_result.resolved_model_name)
        except Exception as e:
            logger.error(f"Compiler unhandled error: {traceback.format_exc()}")

            if hasattr(e, 'span'):
                span = e.span  # type: ignore
            else:
                span = Span(0, len(query))

            if isinstance(e, AbstractInferenceQueryLanguageError):
                errors.add(e)
            else:
                errors.add_unhandled(span=span, cause=e)

            return CompilerResult(plan=None, errors=errors)
