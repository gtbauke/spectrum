# Implementation Plan: IQL Test Suite

This plan outlines the creation of a full-stack test suite for the Inference Query Language (IQL) package. It covers tokenization, parsing, semantic analysis, logical planning, and execution against mock models.

## User Review Required

> [!IMPORTANT]
> This test suite introduces `Hypothesis` for property-based testing. Ensure this library is in the dev-dependencies.
> The `executor` tests require a `MockRegression` class that implements the `reggression` library's API. This mock will be strictly synchronous as per the new requirements.

## Proposed Changes

### Configuration & Fixtures
- [NEW] `packages/inference_query_language/tests/conftest.py`: Root testing configuration and shared fixtures (Compiler and Registry).

### Unit Tests (Pure Domain Logic)
- [NEW] `packages/inference_query_language/tests/tokenizer/test_tokenizer.py`: Tests for lexical analysis.
- [NEW] `packages/inference_query_language/tests/parser/test_parser.py`: Tests for grammar rules and AST integrity.
- [NEW] `packages/inference_query_language/tests/analyzer/test_analyzer.py`: Tests for semantic rules and symbol table resolution.
- [NEW] `packages/inference_query_language/tests/planner/test_planner.py`: Tests for AST-to-LogicalPlan transformations.

### Integration & Execution Tests
- [NEW] `packages/inference_query_language/tests/test_compiler.py`: End-to-end compiler verification.
- [NEW] `packages/inference_query_language/tests/test_executor.py`: Plan interpretation against mock regressions.
- [NEW] `packages/inference_query_language/tests/fuzzing/test_iql_fuzz.py`: Automated edge-case discovery via `Hypothesis`.

## Open Questions

- **Dataset Samples**: Should I include a small CSV sample in `tests/resources` for the `MockRegression` or generate random dataframes during tests?
- **Detailed Error Messages**: Does the current `IqlErrorCollector` store error spans and context sufficiently for assertion in tests?

## Verification Plan

### Automated Tests
- `pytest packages/inference_query_language/tests -v`
- `pytest packages/inference_query_language/tests --cov=iql`

### Manual Verification
- Check that providing a model name missing from the `AnalysisContext` correctly triggers a `ModelNotFoundError` in the test output.
