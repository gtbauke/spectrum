# Tasks: IQL Compiler Refactor

## Phase 1: Foundation (Domain & Registry)

- [ ] **Define Error Collection Structure**
  Create a centralized `IqlErrorCollector` and base `IqlError` classes in `iql/errors/` to support reporting multiple errors at once.
- [ ] **Implement Function Registry**
  Define `FunctionRegistry` in `iql/registry/` to store builtin function signatures and their implementations (e.g., `PREDICT`).

## Phase 2: Analysis & Planning (Core Logic)

- [ ] **Implement Symbol Table**
  Create `SymbolTable` in `iql/analyzer/` to track identifier types and sources during analysis.
- [ ] **Implement Analyzer**
  Build the `Analyzer` visitor to perform semantic validation (symbol resolution, type checking) and collect errors.
- [ ] **Define Logical Plan Nodes**
  Create Pydantic-based `LogicalPlanNode` models in `iql/executor/plan/nodes.py`.
- [ ] **Refactor Planner**
  Update `Planner` in `iql/executor/plan/planner.py` to transform the validated AST into a `LogicalPlan`.

## Phase 3: Execution (Plan Interpretation)

- [ ] **Refactor QueryExecutor**
  Modify `QueryExecutor` in `iql/executor/query_executor.py` to interpret the `LogicalPlan` instead of the AST directly.
- [ ] **Implement Compiler Orchestrator**
  Create `iql/compiler.py` to provide a unified `compile(query_string)` API.

## Phase 4: Integration & Verification

- [ ] **Update Endpoints/Worker (Plan only)**
  Add a section in the docs describing the future integration in `backend` and `worker`.
- [ ] **Comprehensive Testing**
  Write unit tests for `Analyzer`, `Planner`, and `Executor` to verify the new phased pipeline.
