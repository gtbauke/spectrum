# Tasks: IQL Test Suite

## Phase 1: Infrastructure & Tokenizer [Domain]
- [ ] **[NEW] `packages/inference_query_language/tests/conftest.py`**: Define global fixtures and initial `MockRegression`.
    - *Why*: Provides a reusable environment for all subsequent tests, especially mocking the external `reggression` dependency.
- [ ] **[NEW] `packages/inference_query_language/tests/tokenizer/test_tokenizer.py`**: Implement unit tests for basic and edge tokens.
    - *Why*: Ensures the foundation of the pipeline (string to tokens) is bulletproof.

## Phase 2: Parser & AST [Domain]
- [ ] **[NEW] `packages/inference_query_language/tests/parser/test_parser.py`**: Test every IQL command (SELECT, SEARCH, etc.) and syntax error.
    - *Why*: Verifies that the recursive descent / Pratt parser correctly builds the AST for all query modes.

## Phase 3: Analyzer & Planner [Domain]
- [ ] **[NEW] `packages/inference_query_language/tests/analyzer/test_analyzer.py`**: Validate semantic rules (models, columns, functions).
    - *Why*: Catches logical errors in queries (e.g., querying a non-existent model) that syntax checking misses.
- [ ] **[NEW] `packages/inference_query_language/tests/planner/test_planner.py`**: Verify transformation from AST to `LogicalPlan`.
    - *Why*: Ensures the execution plan accurately represents the intention of the AST.

## Phase 4: Integration & Executor [Application]
- [ ] **[NEW] `packages/inference_query_language/tests/test_compiler.py`**: End-to-end tests from query string to `LogicalPlan`.
    - *Why*: Confirms all compiler phases work together seamlessly.
- [ ] **[NEW] `packages/inference_query_language/tests/test_executor.py`**: Execute plans against `MockRegression` and verify result dataframes.
    - *Why*: Validates the actual interpretation and data transformation logic.
- [ ] **[NEW] `packages/inference_query_language/tests/fuzzing/test_iql_fuzz.py`**: Property-based tests for parser robustness.
    - *Why*: Discovers "impossible" edge cases through automated exploration.
