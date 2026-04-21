import pytest

from iql.tokenizer.tokenizer import QueryTokenizer
from iql.parser.parser import InferenceQueryParser
from iql.analyzer.analyzer import AnalysisContext, SemanticAnalyzer
from iql.executor.plan.planner import Planner
from iql.executor.plan.nodes import ScanNode, FilterNode, SearchNode, ProjectNode, ApplyNode, SearchMode
from iql.errors.collector import IqlErrorCollector
from iql.registry.function import create_default_registry


@pytest.fixture
def planner_context(regressions):
    registry = create_default_registry()
    ctx = AnalysisContext(available_model_names=list(
        regressions.keys()), function_registry=registry)
    return ctx


def test_planner_creates_scan_search_project(planner_context):
    query = "SELECT TOP 5 expression FROM model_a"
    tokenizer = QueryTokenizer(query)
    tokens = tokenizer.tokenize()
    parser = InferenceQueryParser(tokens)
    ast = parser.parse_expression()

    analyzer = SemanticAnalyzer(planner_context)
    analysis_result = analyzer.analyze(ast)
    errors = IqlErrorCollector()

    planner = Planner(ast, analysis_result, errors)
    plan = planner.create_plan()

    # Structure: ProjectNode -> SearchNode -> ScanNode
    root = plan.root
    assert isinstance(root, ProjectNode)
    assert root.columns == ["expression"]

    search = root.child
    assert isinstance(search, SearchNode)
    assert search.mode == SearchMode.TOP_N
    assert search.n == 5

    scan = search.child
    assert isinstance(scan, ScanNode)
    assert scan.model_name == "model_a"


def test_planner_includes_filter(planner_context):
    query = "SELECT TOP 5 id FROM model_a WHERE size > 10"
    tokenizer = QueryTokenizer(query)
    tokens = tokenizer.tokenize()
    parser = InferenceQueryParser(tokens)
    ast = parser.parse_expression()

    analysis_result = SemanticAnalyzer(planner_context).analyze(ast)
    planner = Planner(ast, analysis_result, IqlErrorCollector())
    plan = planner.create_plan()

    # Structure: ProjectNode -> SearchNode -> FilterNode -> ScanNode
    search = plan.root.child
    filter_node = search.child
    assert isinstance(filter_node, FilterNode)
    assert "SIZE > 10" in filter_node.conditions or "size > 10" in filter_node.conditions


def test_planner_includes_apply_for_predict(planner_context):
    query = "SELECT PREDICT(x=1.0) FROM model_a"
    tokenizer = QueryTokenizer(query)
    tokens = tokenizer.tokenize()
    parser = InferenceQueryParser(tokens)
    ast = parser.parse_expression()

    analysis_result = SemanticAnalyzer(planner_context).analyze(ast)
    planner = Planner(ast, analysis_result, IqlErrorCollector())
    plan = planner.create_plan()

    # Structure: ProjectNode -> ApplyNode -> SearchNode -> ScanNode
    apply_node = plan.root.child
    assert isinstance(apply_node, ApplyNode)
    assert apply_node.function_name == "PREDICT"
    assert apply_node.arguments == {"x": 1.0}
