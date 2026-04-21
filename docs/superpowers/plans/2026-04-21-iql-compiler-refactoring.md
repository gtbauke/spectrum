# IQL Compiler Refactoring Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Refactor the Inference Query Language (IQL) package to use a Compiler Pattern implementation, supporting generic function calls, aliasing, and variable command results.

**Architecture:** We will split IQL evaluation into Parsing (AST), Semantic Analysis (Logical Plan via Visitor), and Physical Execution. The `QueryExecutor` is streamlined to only process the Logical Plan, isolating parsing rules to the AST layer.

**Tech Stack:** Python 3.12, Pytest

---

### Task 1: Extend Tokenizer for AS Keyword

**Files:**
- Modify: `packages/inference_query_language/iql/tokenizer/token.py`
- Modify: `packages/inference_query_language/iql/tokenizer/tokenizer.py`
- Test: `packages/inference_query_language/tests/tokenizer/test_tokenizer.py` (Assuming structure)

- [ ] **Step 1: Write the failing test for tokenizer**
```python
def test_tokenize_as_keyword():
    tokenizer = QueryTokenizer("SELECT a AS b")
    tokens = tokenizer.tokenize()
    assert any(t.kind == TokenKind.AS for t in tokens)
```
- [ ] **Step 2: Run test to verify it fails**
Run: `uv run pytest packages/inference_query_language/tests/tokenizer/ -v`
Expected: FAIL, unknown token AS

- [ ] **Step 3: Write minimal implementation**
  - Add `AS` to `TokenKind` enum in `token.py`.
  - Add logic in `tokenizer.py` to match 'AS' (case-insensitive) as keyword.
- [ ] **Step 4: Run test to verify it passes**
Run: `uv run pytest packages/inference_query_language/tests/tokenizer/ -v`
Expected: PASS
- [ ] **Step 5: Commit**
Run: `git commit -am "feat: add AS token to tokenizer"`

---

### Task 2: Implement AS Parselet and AST Nodes

**Files:**
- Create: `packages/inference_query_language/iql/parser/ast/alias_node.py`
- Create: `packages/inference_query_language/iql/parser/parselets/as_parselet.py`
- Modify: `packages/inference_query_language/iql/parser/parser.py`
- Modify: `packages/inference_query_language/iql/parser/precedence.py`
- Test: `packages/inference_query_language/tests/parser/test_parser.py`

- [ ] **Step 1: Write the failing test**
```python
def test_parse_alias_expression():
    tokens = QueryTokenizer("SELECT fun() AS f_alias").tokenize()
    parser = InferenceQueryParser(tokens)
    root = parser.parse_expression()
    # assert AST has AliasAstNode mapping to function
```
- [ ] **Step 2: Run test to verify it fails**
Run: `uv run pytest packages/inference_query_language/tests/parser/ -v`
- [ ] **Step 3: Write minimal implementation**
  - Create `AliasAstNode` containing `expression: BaseAstNode` and `alias: IdentifierAstNode`.
  - Add `Precedence.ALIAS`
  - Create `AsParselet(InfixParselet)` that parses left expression and grabs right identifier.
  - Register `TokenKind.AS` -> `AsParselet` in `parser.py`.
- [ ] **Step 4: Run test to verify it passes**
Run: `uv run pytest packages/inference_query_language/tests/parser/ -v`
- [ ] **Step 5: Commit**
Run: `git commit -am "feat: add AST nodes and parselet for ALIAS"`

---

### Task 3: Create Logical Plan Data Models

**Files:**
- Create: `packages/inference_query_language/iql/analyzer/logical_plan.py`

- [ ] **Step 1: Define generic Logical models**
Create models using Pydantic or Python dataclasses that describe explicit commands securely. Example: `LogicalSelectPlan`, `LogicalFunctionCall`, `CommandResult`. Add simple unit tests asserting instantiation works.
- [ ] **Step 2: Write tests for logic instantiation**
- [ ] **Step 3: Verify pass**
- [ ] **Step 4: Commit**
Run: `git commit -am "feat: define logical plan models"`

---

### Task 4: Implement Query Analyzer

**Files:**
- Create: `packages/inference_query_language/iql/analyzer/query_analyzer.py`
- Create: `packages/inference_query_language/iql/analyzer/function_registry.py`
- Test: `packages/inference_query_language/tests/analyzer/test_query_analyzer.py`

- [ ] **Step 1: Write the failing test**
```python
def test_query_analyzer_resolves_functions():
    ast = ... # create mock AST
    analyzer = QueryAnalyzer()
    plan = analyzer.analyze(ast)
    assert isinstance(plan, LogicalSelectPlan)
```
- [ ] **Step 2: Verify test fails**
- [ ] **Step 3: Write implementation**
  - Create `QueryAnalyzer` with a `analyze()` method serving as AST Visitor.
  - Resolve `FunctionCallAstNode` to registry. Standardize aliasing (if no `AS` clause exists, create auto-alias).
- [ ] **Step 4: Run test to verify it passes**
- [ ] **Step 5: Commit**
Run: `git commit -am "feat: add QueryAnalyzer and function registry"`

---

### Task 5: Refactor Query Executor

**Files:**
- Modify: `packages/inference_query_language/iql/executor/query_executor.py`
- Modify: `packages/workers/handlers/inference_run_requested.py`
- Test: `packages/inference_query_language/tests/executor/test_query_executor.py`

- [ ] **Step 1: Write the failing test executing LogicalPlan**
- [ ] **Step 2: Verify failure** (Method missing/changed)
- [ ] **Step 3: Refactor QueryExecutor**
  - Make `QueryExecutor` accept `LogicalPlan` directly.
  - Remove all parser imports from `executor`. Remove AST evaluation.
  - Map logical plan outputs properly, returning a `CommandResult(kind=..., data=...)`.
  - Update `inference_run_requested.py` to pipe `Parser -> Analyzer -> Executor`, and map `CommandResult`.
- [ ] **Step 4: Run all integration tests to catch regressions**
- [ ] **Step 5: Commit**
Run: `git commit -am "refactor: isolate QueryExecutor and update worker pipeline"`
