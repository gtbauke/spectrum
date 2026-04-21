# Specification: IQL Compiler Refactor

## 1. Goal
Refactor the Inference Query Language (IQL) execution pipeline from a single-phase AST-based execution to a modular phased compiler architecture. This will introduce formal Analysis and Planning phases, enabling structural transparency (Execution Plans), easier extensibility for new features, and a robust builtin function registry.

## 2. User Stories
- **As a Developer**, I want the IQL pipeline to have distinct phases (Tokenizer, Parser, Analyzer, Planner, Executor) so that I can easily add new language features or builtin functions without modifying the core execution logic.
- **As a Developer**, I want a formal Function Registry so that I can define builtin functions and their signatures in a centralized place.
- **As a Power User**, I want to see the Execution Plan of my IQL query so that I can understand how my query is being processed and debug potential performance or logic issues.
- **As a System**, I want the IQL Analyzer to validate types and symbols before execution so that I can report all errors to the user at once rather than failing midway through execution.

## 3. Acceptance Criteria
- [ ] Implement a `FunctionRegistry` that stores builtin function signatures and implementations.
- [ ] Implement an `Analyzer` phase that performs symbol resolution and type checking, collecting all errors.
- [ ] Implement a `Planner` phase that transforms the AST and analysis metadata into a `LogicalPlan` comprised of high-level operators.
- [ ] Implement an `Executor` phase that traverses the `LogicalPlan` and interacts with the `Reggression` object.
- [ ] Update the `IQL` entry point to orchestrate these new phases.
- [ ] Ensure all errors (AST, semantic, planning, execution) are collected and reported using a consistent error structure.
- [ ] Provide a way to serialize the `LogicalPlan` for future frontend rendering.

## 4. Scope
- **In-Scope**:
    - Complete redesign of the `packages/inference_query_language` internal structure.
    - Implementation of `Analyzer`, `Planner`, and `LogicalPlan` (tree of operators).
    - Refactor of `QueryExecutor` to consume `LogicalPlan`.
    - Function Registry implementation.
    - Centralized error collection and reporting.
- **Out-of-Scope**:
    - Actual integration into the `backend` and `frontend` packages (reserved for future work).
    - Implementation of new complex language features (like JOINs) not already present in the current IQL.
    - Performance optimizations (e.g., Physical Planning/Cost-based optimization).

## 5. Affected Packages
- `packages/inference_query_language`: Primary focus of the refactor.
- `packages/core` (indirectly): For potential shared IQL DTOs if needed.
- `packages/backend` / `packages/workers` (indirectly): Future integration points.
