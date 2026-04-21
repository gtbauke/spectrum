# Specification: IQL Test Suite

## 1. Goal
Establish a comprehensive testing infrastructure for the Inference Query Language (IQL) package. This suite will ensure the correctness of every phase of the compilation and execution pipeline, from string tokenization to final interpretation against symbolic regression models.

## 2. User Stories
- **As a Developer**, I want to verify that the `Tokenizer` and `Parser` correctly handle all IQL syntax variants so I can confidently add new language features.
- **As a Developer**, I want to ensure the `Analyzer` catches semantic errors (like missing models or invalid columns) before execution to provide clear feedback to the user.
- **As a Developer**, I want to test the `QueryExecutor` against mock models to verify that search modes (TOP N, PARETO, DISTRIBUTION) and functions (PREDICT) return expected results.
- **As a Developer**, I want property-based tests to uncover edge cases in the parser that I might have missed in manual test cases.

## 3. Acceptance Criteria
- [ ] **Unit Tests**: Full coverage for `Tokenizer`, `Parser`, `Analyzer`, and `Planner`.
- [ ] **Integration Tests**: End-to-end tests for `IqlCompiler` and `QueryExecutor`.
- [ ] **Mock Infrastructure**: A `MockRegression` class that implements the `reggression` library interface.
- [ ] **Error Coverage**: Tests for all custom exceptions in `iql.errors`, `iql.analyzer.errors`, and `iql.executor.errors`.
- [ ] **Fuzzing**: A set of property-based tests using `Hypothesis` for the parser.
- [ ] **Performance**: The test suite should run in less than 30 seconds.

## 4. Scope
- **In-Scope**:
    - `packages/inference_query_language/tests/` directory and its children.
    - Mocking the `reggression` library and `PredictionEvaluationService`.
    - Unit tests for all phases of `IqlCompiler`.
    - Integration tests for `QueryExecutor`.
- **Out-of-Scope**:
    - Testing the database layer or SQLAlchemy models (handled by DB Layer tests).
    - Testing the React frontend components (handled by Vitest).
    - Testing the RabbitMQ worker orchestration.
