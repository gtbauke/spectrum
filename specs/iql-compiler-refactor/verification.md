# Verification Plan: IQL Compiler Refactor

## 1. Automated Tests

### Analyzer Tests
Verify that the analyzer correctly identifies symbols and type mismatches.
```python
def test_analyzer_identifies_missing_model():
    query = "SELECT id FROM non_existent_model"
    # ... assert that Analyzer adds ModelNotFoundError to errors
```

### Planner Tests
Verify that the planner produces a correct `LogicalPlan` for various query types.
```python
def test_planner_generates_correct_top_n_plan():
    query = "SELECT TOP 10 id FROM model_1 WHERE size > 5"
    # ... assert that LogicalPlan has Scan -> Filter -> Search(TOP) -> Project structure
```

### Executor Tests
Verify that the new executor produces the same results as the old one.
```python
def test_executor_equivalence():
    query = "SELECT id, expression FROM model_1 TOP 5"
    # ... compare results of old vs new execution pipeline
```

## 2. Manual Checklist
- [ ] **Phase 1**: Verify `FunctionRegistry` can register and retrieve functions.
- [ ] **Phase 2**: Run `Analyzer` on a valid query and confirm empty error list.
- [ ] **Phase 3**: Run `Planner` and inspect the serialized `LogicalPlan` JSON.
- [ ] **Phase 4**: Run a full end-to-end query from string to `InferenceResultList` using a mock `Reggression` object.
