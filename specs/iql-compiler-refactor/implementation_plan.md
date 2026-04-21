# Implementation Plan: IQL Compiler Refactor

This plan outlines the modular redesign of the IQL execution pipeline, moving from a single-phase AST interpretation to a structured compiler with Analysis and Planning phases.

## User Review Required

> [!IMPORTANT]
> The `LogicalPlan` will be implemented using Pydantic models to ensure it is easily serializable for future frontend rendering.
> All internal errors will be collected and reported via an `IqlErrorCollector`, facilitating a better developer experience.

## Proposed Changes

### 1. Registry (Builtin Functions)
Introduce a centralized registry for IQL functions.

#### [NEW] [function.py](file:///home/gusta/dev/spectrum/packages/inference_query_language/iql/registry/function.py)
Defines `FunctionDefinition` and `FunctionRegistry`.

### 2. Analyzer (Semantic Validation)
Implement the Analysis phase to validate symbols and types.

#### [NEW] [symbol_table.py](file:///home/gusta/dev/spectrum/packages/inference_query_language/iql/analyzer/symbol_table.py)
Tracks identifiers, types, and scopes.

#### [NEW] [analyzer.py](file:///home/gusta/dev/spectrum/packages/inference_query_language/iql/analyzer/analyzer.py)
The primary visitor for semantic analysis.

### 3. Planner (Logical Plan Generation)
Implement the Planning phase to transform AST into a tree of operators.

#### [NEW] [nodes.py](file:///home/gusta/dev/spectrum/packages/inference_query_language/iql/executor/plan/nodes.py)
Defines Pydantic-based `LogicalPlanNode` types (Scan, Filter, Project, Apply, Search).

#### [MODIFY] [planner.py](file:///home/gusta/dev/spectrum/packages/inference_query_language/iql/executor/plan/planner.py)
Refactor to produce a `LogicalPlan` instead of just wrapping the AST.

### 4. Executor (Plan Interpretation)
Refactor the executor to interpret the `LogicalPlan`.

#### [MODIFY] [query_executor.py](file:///home/gusta/dev/spectrum/packages/inference_query_language/iql/executor/query_executor.py)
Logic to traverse and execute `LogicalPlanNode`s against a `Reggression` object.

### 5. Orchestration (Compiler Entry Point)

#### [NEW] [compiler.py](file:///home/gusta/dev/spectrum/packages/inference_query_language/iql/compiler.py)
A high-level API to orchestrate `tokenize -> parse -> analyze -> plan`.

## Open Questions

> [!NOTE]
> No critical open questions remain after the interview phase.

## Verification Plan

### Automated Tests
- `pytest packages/inference_query_language/tests`: A new suite of tests for individual phases (Analyzer, Planner) and end-to-end execution.

### Manual Verification
- Execute existing IQL queries via a scratch script to ensure the new pipeline produces identical results to the previous one.
